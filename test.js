// const {Builder, By, Key, Util} = require("selenium-webdriver");
// require("chromedriver");

// async function example() {
//     let driver = await new Builder().forBrowser("chrome").build();
//     await driver.get("https://connect.wofford.edu/myWofford/registrar/courseSchedule.aspx");
//     await driver.findElement(By.name("q")).sendKeys("Selenium Test", Key.RETURN);
// }

// example();



// const { Builder, By } = require('selenium-webdriver');
// require("chromedriver");


// (async function scrapeTable() {
//   // Launch browser
//   let driver = await new Builder().forBrowser('chrome').build();

//   try {
//     // Open the URL
//     await driver.get('https://connect.wofford.edu/myWofford/registrar/courseSchedule.aspx');

//     // Find the table by ID
//     const rows = await driver.findElements(By.css('tbody tr'));

//     for (let i = 0; i < rows.length; i++) {
//       const cells = await rows[i].findElements(By.css('th, td'));

//       const rowData = [];
//       for (let cell of cells) {
//         const text = await cell.getText();
//         rowData.push(text);
//       }

//       console.log(rowData.join(' | '));
//     }
//   } finally {
//     // Close browser after scraping
//     await driver.quit();
//   }
// })();




// Test Try:

const { Builder, By } = require('selenium-webdriver');
require("chromedriver");


async function scrapeTest() {
    // Launch browser
    let driver = await new Builder().forBrowser('chrome').build();

    // Open the URL
    await driver.get('https://connect.wofford.edu/myWofford/registrar/courseSchedule.aspx');

    // Find the table by HTML element
    const rows = await driver.findElements(By.css("tbody tr"));
    const test = await rows[0].getText();
    const details = test.split(" ");
    details.splice(4, 7);
    console.log(details);
    // course_dict = {};

    // for(let i = 0; i < rows.length; i++) {

    // }




    await driver.quit();
}

scrapeTest();


// Next to do: Merge the names into a single index.

