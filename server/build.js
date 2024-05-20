const fs = require('fs');
const path = require('path');

// Example build script
const buildDir = path.join(__dirname, 'dist');

if (!fs.existsSync(buildDir)){
    fs.mkdirSync(buildDir);
}

// Write some output to the dist directory
fs.writeFileSync(path.join(buildDir, 'index.js'), 'console.log("Hello, world!");');