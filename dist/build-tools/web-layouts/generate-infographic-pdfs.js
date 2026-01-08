#!/usr/bin/env node
/**
 * Generate beautiful infographic PDFs from HTML layouts using Puppeteer
 * Creates magazine-quality PDFs with modern design
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs').promises;

// Configuration
const layouts = [
    {
        name: 'token-cost-infographic',
        input: 'token-cost-infographic.html',
        output: 'aps-token-calculator-infographic.pdf',
        title: 'APS Token Cost Calculator',
        format: 'A4'
    },
    {
        name: 'error-codes-visual',
        input: 'error-codes-visual.html',
        output: 'aps-error-codes-visual.pdf',
        title: 'APS Error Codes Visual Guide',
        format: 'A4'
    },
    {
        name: 'oauth-flow-diagram',
        input: 'oauth-flow-diagram.html',
        output: 'oauth-flow-infographic.pdf',
        title: '3-Legged OAuth Flow',
        format: 'A4'
    }
];

async function generatePDF(layout) {
    console.log(`📄 Generating: ${layout.title}`);
    
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Load HTML file
        const htmlPath = path.join(__dirname, layout.input);
        const htmlContent = await fs.readFile(htmlPath, 'utf8');
        
        // Set content with base URL for relative resources
        await page.setContent(htmlContent, {
            waitUntil: 'networkidle0',
            baseURL: `file://${__dirname}/`
        });
        
        // Wait for any animations or dynamic content
        await page.waitForTimeout(1000);
        
        // Generate PDF with high quality settings
        const outputPath = path.join(__dirname, '..', '..', 'pdfs', layout.output);
        await page.pdf({
            path: outputPath,
            format: layout.format,
            printBackground: true,
            margin: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            },
            displayHeaderFooter: false,
            preferCSSPageSize: true,
            scale: 1,
            printBackground: true
        });
        
        // Also copy to docs/pdfs for GitHub Pages
        const docsPath = path.join(__dirname, '..', '..', 'docs', 'pdfs', layout.output);
        await fs.copyFile(outputPath, docsPath);
        
        // Get file size
        const stats = await fs.stat(outputPath);
        const sizeMB = (stats.size / (1024 * 1024)).toFixed(1);
        
        console.log(`✅ Generated: ${layout.output} (${sizeMB}MB)`);
        console.log(`   📋 Copied to: docs/pdfs/${layout.output}`);
        
        return true;
    } catch (error) {
        console.error(`❌ Error generating ${layout.name}:`, error);
        return false;
    } finally {
        await browser.close();
    }
}

async function generateAllPDFs() {
    console.log('🚀 Puppeteer Infographic PDF Generator');
    console.log('=====================================');
    console.log('Creating magazine-quality PDFs from modern web layouts\n');
    
    let successCount = 0;
    
    for (const layout of layouts) {
        // Check if input file exists
        const inputPath = path.join(__dirname, layout.input);
        try {
            await fs.access(inputPath);
            if (await generatePDF(layout)) {
                successCount++;
            }
        } catch {
            console.log(`⚠️  Input file not found: ${layout.input}`);
        }
        console.log(); // Add spacing between PDFs
    }
    
    console.log('=====================================');
    console.log(`✅ Successfully generated: ${successCount}/${layouts.length} PDFs`);
    
    if (successCount > 0) {
        console.log('\n🎨 Features Applied:');
        console.log('  ✓ Modern gradient designs');
        console.log('  ✓ Interactive-looking elements');
        console.log('  ✓ Professional typography');
        console.log('  ✓ Data visualizations');
        console.log('  ✓ RAPS branding throughout');
        console.log('  ✓ Print-optimized colors');
        
        console.log('\n📤 Distribution Ready:');
        console.log('  • High-quality infographic PDFs');
        console.log('  • Perfect for marketing materials');
        console.log('  • Conference handouts');
        console.log('  • Social media sharing');
    }
}

// Check if Puppeteer is installed
try {
    require.resolve('puppeteer');
    generateAllPDFs().catch(console.error);
} catch {
    console.error('❌ Puppeteer not installed!');
    console.log('\n📦 Install Puppeteer:');
    console.log('   npm install puppeteer');
    console.log('\n💡 Or install globally:');
    console.log('   npm install -g puppeteer');
    process.exit(1);
}