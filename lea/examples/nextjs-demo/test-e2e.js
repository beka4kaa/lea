#!/usr/bin/env node

/**
 * E2E Test: Fetch UI components from Lea and generate Next.js app
 */

const fs = require('fs');
const path = require('path');

const LEA_API_URL = 'http://localhost:8000';

// MCP JSON-RPC client
async function mcpCall(method, params = {}) {
  const response = await fetch(`${LEA_API_URL}/mcp`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: Math.floor(Math.random() * 1000),
      method,
      params,
    }),
  });

  const data = await response.json();
  
  if (data.error) {
    throw new Error(`MCP Error: ${data.error.message}`);
  }
  
  return data.result;
}

// Tool call wrapper
async function callTool(toolName, arguments_) {
  const result = await mcpCall('tools/call', {
    name: toolName,
    arguments: arguments_,
  });
  
  if (result.content && result.content[0] && result.content[0].text) {
    return JSON.parse(result.content[0].text);
  }
  
  return result;
}

async function main() {
  console.log('🚀 Starting Lea Next.js E2E Test...');
  
  try {
    // Step 1: Initialize MCP connection
    console.log('1. Initializing MCP connection...');
    const initResult = await mcpCall('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: {
        name: 'Next.js E2E Test',
        version: '1.0.0',
      },
    });
    console.log(`✓ Connected to ${initResult.serverInfo.name} v${initResult.serverInfo.version}`);

    // Step 2: Get Auth Block
    console.log('2. Fetching Auth Block...');
    const authBlock = await callTool('get_block', {
      block_type: 'auth',
      target: 'nextjs',
      style: 'tailwind',
    });
    console.log(`✓ Got ${authBlock.name}: ${authBlock.description}`);

    // Step 3: Get Navbar Block
    console.log('3. Fetching Navbar Block...');
    const navbarBlock = await callTool('get_block', {
      block_type: 'navbar',
      target: 'nextjs',
      style: 'tailwind',
    });
    console.log(`✓ Got ${navbarBlock.name}: ${navbarBlock.description}`);

    // Step 4: Get Hero Block
    console.log('4. Fetching Hero Block...');
    const heroBlock = await callTool('get_block', {
      block_type: 'hero',
      target: 'nextjs',
      style: 'tailwind',
    });
    console.log(`✓ Got ${heroBlock.name}: ${heroBlock.description}`);

    // Step 5: Get Pricing Block
    console.log('5. Fetching Pricing Block...');
    const pricingBlock = await callTool('get_block', {
      block_type: 'pricing',
      target: 'nextjs',
      style: 'tailwind',
    });
    console.log(`✓ Got ${pricingBlock.name}: ${pricingBlock.description}`);

    // Step 6: Generate install plan
    console.log('6. Generating install plan...');
    const installPlan = await callTool('install_plan', {
      component_ids: ['auth', 'navbar', 'hero', 'pricing'],
      target: 'nextjs',
      package_manager: 'npm',
    });
    console.log(`✓ Dependencies: ${installPlan.runtime_dependencies.join(', ')}`);

    // Step 7: Create component files
    console.log('7. Creating component files...');
    
    const blocks = [authBlock, navbarBlock, heroBlock, pricingBlock];
    const generatedFiles = [];
    
    for (const block of blocks) {
      for (const file of block.files) {
        const fullPath = path.join('components', file.path.split('/').slice(-1)[0]);
        
        // Ensure components directory exists
        const dir = path.dirname(fullPath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        
        // Write component file
        fs.writeFileSync(fullPath, file.content);
        generatedFiles.push(fullPath);
        console.log(`  ✓ Created ${fullPath}`);
      }
    }

    // Step 8: Create main page using all components
    console.log('8. Creating main page...');
    const mainPageContent = `import React from 'react';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import PricingTable from '../components/PricingTable';
import LoginForm from '../components/LoginForm';
import './globals.css';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Hero />
      <div className="py-16">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Choose Your Plan</h2>
          <PricingTable />
        </div>
      </div>
      <div className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Sign In</h2>
          <LoginForm />
        </div>
      </div>
    </div>
  );
}`;

    fs.writeFileSync('app/page.tsx', mainPageContent);
    console.log('  ✓ Created app/page.tsx');

    // Step 9: Create layout file
    console.log('9. Creating layout file...');
    const layoutContent = `import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Lea Demo App',
  description: 'Generated with Lea UI Components',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}`;

    fs.writeFileSync('app/layout.tsx', layoutContent);
    console.log('  ✓ Created app/layout.tsx');

    // Step 10: Verify generated code
    console.log('10. Verifying generated code...');
    let totalIssues = 0;
    
    for (const filePath of [...generatedFiles, 'app/page.tsx', 'app/layout.tsx']) {
      if (filePath.endsWith('.tsx')) {
        const code = fs.readFileSync(filePath, 'utf8');
        const verifyResult = await callTool('verify', {
          code,
          framework: 'nextjs',
          check_imports: true,
          check_syntax: true,
        });
        
        const issues = verifyResult.issues.filter(i => i.severity === 'error');
        totalIssues += issues.length;
        
        if (issues.length > 0) {
          console.log(`  ⚠️  ${filePath}: ${issues.length} error(s)`);
          issues.forEach(issue => {
            console.log(`     - ${issue.message}`);
          });
        } else {
          console.log(`  ✓ ${filePath}: Clean`);
        }
      }
    }

    console.log('\\n📊 Generation Summary:');
    console.log(`✓ Generated ${generatedFiles.length + 2} files`);
    console.log(`✓ Total dependencies: ${installPlan.runtime_dependencies.length}`);
    console.log(`${totalIssues === 0 ? '✓' : '⚠️'} Code issues: ${totalIssues}`);
    console.log(`✓ Ready for: npm run build`);

    console.log('\\n🎉 E2E Test completed successfully!');
    console.log('\\nNext steps:');
    console.log('  1. npm install');
    console.log('  2. npm run build');
    console.log('  3. npm run start');

  } catch (error) {
    console.error('❌ E2E Test failed:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}