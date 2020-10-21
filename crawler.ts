import * as puppeteer from 'puppeteer';
import * as fs from 'fs';
import * as readline from 'readline';

import { LoadEvent } from 'puppeteer';

const createDirectory = (folderPath: string) => fs.existsSync(folderPath) || fs.mkdirSync(folderPath);

const PATH = "download_data";

const readIndex = async(fn: string) => {

    let set = new Set();

    if (!fs.existsSync(fn)) {
        fs.writeFile(fn, "", (err) => {
            if (err) return console.error(err);
        });
    }

    try {
        let index_rs = fs.createReadStream(fn);

        const readInterface = readline.createInterface({
            input: index_rs,
            output: null,
        });

        for await (const line of readInterface){
            set.add(line);
        }
    } catch {

    }
    
    return set;
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const main = async() => {

    createDirectory(`${PATH}`)
    createDirectory(`${PATH}/fasta`);
    let index = readIndex(`${PATH}/index`);

    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();

    await page.setViewport({
        width: 1440,
        height: 3000,
        deviceScaleFactor: 0.5,
    });

    const waitUntil: LoadEvent[] = ['load', 'domcontentloaded', 'networkidle0']


    // step 0: go to login page
    await page.goto('https://www.epicov.org/epi3/start', { waitUntil });
    await page.waitForFunction(() => {
        try {
            return typeof window["sys"].getC(
                document.querySelectorAll('div[cid]')[1].getAttribute('cid')
            ).call == "function";
        } catch {
            return false;
        }
    });

    // step 1: login
    await page.evaluate(() => {
        try {
            const tmp_cid = document.querySelectorAll('div[cid]')[1].getAttribute('cid');
            window["sys"].getC(tmp_cid).call(
                'doLogin',
                {'login': "", "hash": ""}
                );
        } catch {
            console.error('doLogin failed');
        }
    });

    await page.waitForNavigation({ waitUntil });
    
    // step 2: to browse page
    await page.waitForSelector('div[onclick*="BrowsePage"]');
    await page.evaluate(`document.querySelector('div[onclick*="BrowsePage"]').click()`);

    // step 4: to virus page
    const limit = 10;
    let count = 0;
    while(true){
        
        await sleep(5000);
        await page.waitForSelector('.yui-dt-rec');

        const virusCount: number = await page.evaluate(() => {
            return document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec').length;
        });
        
        for (let i=0; i<virusCount; i++){
            await page.waitForSelector('.yui-dt-rec');
    
            const id: string = await page.evaluate((i: number) => {
                return document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec')[i].querySelectorAll('td')[3].textContent;
            }, i);
            if ((await index).has(id)) {
                continue;
            }

            // get info of host and collection data and location
            const host: string = await page.evaluate((i: number) => {
                return document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec')[i].querySelectorAll('td')[8].textContent;
            }, i);

            const date: string = await page.evaluate((i: number) => {
                return document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec')[i].querySelectorAll('td')[4].textContent;
            }, i);

            const location: string = await page.evaluate((i: number) => {
                return document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec')[i].querySelectorAll('td')[9].textContent;
            }, i);

            const seq_length: number = await page.evaluate((i: number) => {
                return parseInt(document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec')[i].querySelectorAll('td')[7].textContent, 10);
            }, i);
            
            const month = date.slice(5,7)
            
            if (month != "05" && month != "06" && month != "07") {
                continue;
            }

            // get coordinate of item and click
            const { y, x }: any = await page.evaluate((i: number) => {
                const { top, left } = document.querySelectorAll('div[cid] .yui-dt-data .yui-dt-rec')[i].querySelectorAll('td')[3].getBoundingClientRect();
                return { x: left, y: top };
            }, i);
    
            await page.mouse.click(x, y);
    
            // wait until iframe exists
            await page.waitForFunction(() => {
                try {
                    return typeof document.getElementsByTagName('iframe')[0].contentDocument.getElementsByTagName('pre')[0].textContent == 'string';
                } catch {
                    return false;
                }
            });

            // get iframe 
            
            let iframeContent: string = "";

            while (iframeContent.length < seq_length) {

                await sleep(5000);

                iframeContent = await page.evaluate(
                    `document.getElementsByTagName('iframe')[0].contentDocument.getElementsByTagName('pre')[0].childNodes[0].nodeValue`,
                );

            }

            if(iframeContent.indexOf(id) == -1){
                i--;
                continue;
            }
    
            fs.writeFile(`${PATH}/fasta/${id}.fasta`, iframeContent, (err) => {
                if (err) return console.error(err);
            });

            fs.writeFile(`${PATH}/fasta/${id}.info`, date + "\n" + host + "\n" + location, (err) => {
                if (err) return console.error(err);
            })

            fs.appendFile(`${PATH}/index`, id + "\n", (err) => {
                if (err) return console.error(err);
            });
            
            (await index).add(id)

            count++;

            if(count >= limit){
                break;
            }

            await sleep(5000);
            await page.evaluate(`window.history.back()`);
            await sleep(10000);
        }

        if(count >= limit){
            break;
        }

        await page.evaluate(`$("a.yui-pg-next")[0].click()`);
    }

    await browser.close();

}

main();
