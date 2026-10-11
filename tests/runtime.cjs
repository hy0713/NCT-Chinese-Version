// Standard npm installation first; the desktop's bundled runtime is a fallback.
const path=require('path');
let playwrightPath=process.env.NCT_PLAYWRIGHT;
if(!playwrightPath)try{playwrightPath=path.dirname(require.resolve('playwright/package.json'));}
catch(_){throw new Error('Install dev dependencies with npm install, or set NCT_PLAYWRIGHT.');}
module.exports={...require(playwrightPath),babel:require(process.env.NCT_BABEL||path.join(playwrightPath,'lib/transform/babelBundle.js'))};
