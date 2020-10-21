const fs = require('fs');
const path = require('path');
const moment = require('moment');

export const sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export const currentTimeInStr = (formattedString=undefined) => {
  return moment().format(formattedString || 'YYYYMMDD_hhmmss.SSS');
};

export const currentTimeInMilliseconds = () => {
  return moment().format('x');
}

const writeFile = (path, data, opts = 'utf8') =>
  new Promise((resolve, reject) => {
    fs.writeFile(path, data, opts, (err) => {
      if (err) reject(err)
      else resolve()
    })
  })


export const createDirectory = (folderPath) => {
  return fs.existsSync(folderPath) || fs.mkdirSync(folderPath);
}

export const takeScreenshot = async (Page, name='scresnshot') => {
  const ss = await Page.captureScreenshot({ format: 'png', fromSurface: true });

  await writeFile(`${name}.png`, ss.data, 'base64');
};

export const fillElementWithValue = async (Runtime, elementID, value) => {
  await Runtime.evaluate({
    expression: `$('#${elementID}')[0].value = "${value}";`
  });
};


export const waitUntilExpressionExists = async (Runtime, expression) => {
  const limit = 120;
  let counter = 0;
  while (true) {
    await sleep(1000);
    let result = await Runtime.evaluate({ expression: expression });
    if (
      result != undefined &&
      result.result != undefined &&
      result.result.type != 'undefined' &&
      result.result.subtype != undefined &&
      result.result.subtype != "error"
    ) {
      break;
    }

    counter += 1;
    if (counter > limit) {
      break;
    }
  }
  return counter > limit;
};


export const waitUntilElementExists = async (Runtime, elementID) => {
  const limit = 90;
  let counter = 0;
  while (true) {
    await sleep(1000);
    let result = await Runtime.evaluate({ expression: `$('#${elementID}')[0]` });
    if (
      result != undefined &&
      result.result != undefined &&
      result.result.subtype == "node"
    ) {
      break;
    }

    counter += 1;
    if (counter > limit) {
      break;
    }
  }
  return counter > limit;
};

export const runJavascript = async (Runtime, js) => {
  let result = await Runtime.evaluate({ expression: js });
  try {
    return result.result.value;
  } catch {
    return undefined;
  }
};

export const checkIfExpressionExists = async (Runtime, expression) => {
  let result = await Runtime.evaluate({ expression: expression });
  console.log(result)
  console.log(result.result.type);
  if(result.result.type == 'undefined'){
    return false;
  } else {
    return true;
  }
}

export default {
  sleep,
  currentTimeInStr,
  takeScreenshot,
  waitUntilElementExists,
  runJavascript,
  createDirectory,
  checkIfExpressionExists,
};

