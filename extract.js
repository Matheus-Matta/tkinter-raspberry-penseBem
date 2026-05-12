const fs = require('fs');

['021', '081', '131'].forEach(num => {
  let content = fs.readFileSync(`./src/gabarito/${num}.ts`, 'utf8');
  content = content.replace(/import.*?;\n/g, '');
  content = content.replace(/export type.*?;\n/g, '');
  content = content.replace(/export const GABARITO_PENSE_BEM.*?=\s*/, '');
  content = content.replace(/;\s*$/, '');
  
  try {
    const obj = eval(`(${content})`);
    fs.writeFileSync(`./data/${num}.json`, JSON.stringify(obj, null, 2));
    console.log(`Saved ${num}.json`);
  } catch (e) {
    console.error(`Error processing ${num}:`, e);
  }
});
