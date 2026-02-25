// ============================================================
// AUTODESK FORUM EXPLORER - Bookmarklet
// ============================================================
// 
// HOW TO USE:
// 1. Go to https://forums.autodesk.com
// 2. Open browser DevTools (F12 or Cmd+Option+I)
// 3. Go to Console tab
// 4. Paste this ENTIRE script
// 5. Press Enter
//
// FEATURES:
// - Force-directed graph visualization of all forums
// - Filter by type (category, idea, forum, blog, etc.)
// - Search boards by name
// - Click any board to see top 10 posts with kudos/views
// - Drag nodes to rearrange
// - Zoom and pan the graph
//
// Part of raps-research: https://github.com/dmytro-yemelianov/raps-research
// ============================================================

(async function() {
    'use strict';
    
    // Remove existing if re-running
    const existing = document.getElementById('forum-explorer-overlay');
    if (existing) existing.remove();
    
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'forum-explorer-overlay';
    overlay.innerHTML = `
        <style>
            #forum-explorer-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: #0a0a0f;
                z-index: 999999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                color: #e0e0e0;
                overflow: hidden;
            }
            #fe-app { display: flex; height: 100vh; }
            #fe-sidebar { width: 320px; background: #12121a; border-right: 1px solid #2a2a3a; display: flex; flex-direction: column; }
            #fe-header { padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; }
            #fe-header h1 { margin: 0; font-size: 1.2rem; color: white; }
            #fe-header small { color: rgba(255,255,255,0.7); font-size: 0.75rem; display: block; margin-top: 4px; }
            #fe-close { position: absolute; top: 15px; right: 15px; background: rgba(255,255,255,0.2); border: none; color: white; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; font-size: 18px; }
            #fe-close:hover { background: rgba(255,255,255,0.3); }
            #fe-controls { padding: 15px; border-bottom: 1px solid #2a2a3a; }
            #fe-controls label { display: block; font-size: 0.75rem; color: #888; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
            #fe-search { width: 100%; padding: 10px; background: #1a1a25; border: 1px solid #2a2a3a; border-radius: 6px; color: #e0e0e0; margin-bottom: 15px; font-size: 14px; }
            #fe-search:focus { outline: none; border-color: #667eea; }
            .fe-checkbox-group { display: flex; flex-wrap: wrap; gap: 8px; }
            .fe-checkbox-item { display: flex; align-items: center; gap: 5px; padding: 5px 10px; background: #1a1a25; border-radius: 4px; font-size: 0.8rem; cursor: pointer; transition: background 0.2s; }
            .fe-checkbox-item:hover { background: #252535; }
            .fe-dot { width: 8px; height: 8px; border-radius: 50%; }
            #fe-stats { padding: 15px; background: #0d0d12; border-bottom: 1px solid #2a2a3a; }
            .fe-stat { display: flex; justify-content: space-between; padding: 5px 0; font-size: 0.85rem; }
            .fe-stat-label { color: #888; }
            .fe-stat-value { color: #667eea; font-weight: 600; }
            #fe-list { flex: 1; overflow-y: auto; padding: 10px; }
            .fe-board-item { padding: 10px; margin-bottom: 6px; background: #1a1a25; border-radius: 6px; cursor: pointer; border-left: 3px solid transparent; transition: all 0.2s; }
            .fe-board-item:hover { background: #252535; transform: translateX(3px); }
            .fe-board-item.selected { border-left-color: #667eea; background: #252540; }
            .fe-board-title { font-size: 0.85rem; font-weight: 500; margin-bottom: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .fe-board-meta { font-size: 0.7rem; color: #666; }
            .fe-badge { padding: 2px 6px; border-radius: 3px; font-size: 0.65rem; text-transform: uppercase; margin-right: 8px; }
            #fe-graph-container { flex: 1; position: relative; background: radial-gradient(circle at center, #12121a 0%, #0a0a0f 100%); }
            #fe-graph { width: 100%; height: 100%; }
            #fe-tooltip { position: absolute; padding: 12px 16px; background: #1a1a25; border: 1px solid #2a2a3a; border-radius: 8px; font-size: 0.85rem; pointer-events: none; opacity: 0; max-width: 300px; z-index: 100; box-shadow: 0 10px 40px rgba(0,0,0,0.5); transition: opacity 0.15s; }
            #fe-tooltip.visible { opacity: 1; }
            #fe-tooltip h3 { margin: 0 0 8px; font-size: 0.9rem; color: #fff; }
            #fe-tooltip-info { font-size: 0.8rem; color: #888; line-height: 1.5; }
            #fe-tooltip a { color: #667eea; text-decoration: none; display: block; margin-top: 8px; }
            #fe-tooltip a:hover { text-decoration: underline; }
            #fe-legend { position: absolute; bottom: 20px; left: 20px; background: #12121a; border: 1px solid #2a2a3a; border-radius: 8px; padding: 15px; }
            #fe-legend h4 { margin: 0 0 10px; font-size: 0.75rem; color: #888; text-transform: uppercase; }
            .fe-legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 0.8rem; }
            .fe-legend-dot { width: 12px; height: 12px; border-radius: 50%; }
            #fe-detail { position: absolute; right: 20px; top: 20px; width: 350px; background: #12121a; border: 1px solid #2a2a3a; border-radius: 12px; padding: 20px; display: none; max-height: 80vh; overflow-y: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
            #fe-detail.visible { display: block; }
            #fe-detail h2 { margin: 0 0 15px; font-size: 1rem; padding-right: 30px; }
            #fe-detail-close { position: absolute; top: 15px; right: 15px; background: none; border: none; color: #666; font-size: 1.2rem; cursor: pointer; }
            #fe-detail-close:hover { color: #fff; }
            .fe-message { padding: 10px; margin-bottom: 8px; background: #1a1a25; border-radius: 6px; }
            .fe-message-title { font-size: 0.85rem; margin-bottom: 5px; line-height: 1.4; }
            .fe-message-stats { font-size: 0.75rem; color: #666; }
            #fe-loading { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
            .fe-spinner { width: 50px; height: 50px; border: 3px solid #2a2a3a; border-top-color: #667eea; border-radius: 50%; animation: fe-spin 1s linear infinite; margin: 0 auto 15px; }
            @keyframes fe-spin { to { transform: rotate(360deg); } }
            #fe-list::-webkit-scrollbar { width: 6px; }
            #fe-list::-webkit-scrollbar-track { background: #0a0a0f; }
            #fe-list::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 3px; }
        </style>
        <div id="fe-app">
            <div id="fe-sidebar">
                <div id="fe-header">
                    <button id="fe-close">×</button>
                    <h1>Forum Explorer</h1>
                    <small>Autodesk Community API Visualization</small>
                </div>
                <div id="fe-controls">
                    <label>Search</label>
                    <input type="text" id="fe-search" placeholder="Filter boards...">
                    <label>Filter by Type</label>
                    <div class="fe-checkbox-group" id="fe-filters"></div>
                </div>
                <div id="fe-stats">
                    <div class="fe-stat"><span class="fe-stat-label">Categories</span><span class="fe-stat-value" id="fe-stat-cat">-</span></div>
                    <div class="fe-stat"><span class="fe-stat-label">Boards</span><span class="fe-stat-value" id="fe-stat-board">-</span></div>
                    <div class="fe-stat"><span class="fe-stat-label">Ideas Boards</span><span class="fe-stat-value" id="fe-stat-idea">-</span></div>
                </div>
                <div id="fe-list"></div>
            </div>
            <div id="fe-graph-container">
                <div id="fe-loading"><div class="fe-spinner"></div><div>Loading forum data...</div></div>
                <svg id="fe-graph"></svg>
                <div id="fe-tooltip"><h3></h3><div id="fe-tooltip-info"></div></div>
                <div id="fe-legend">
                    <h4>Node Types</h4>
                    <div class="fe-legend-item"><div class="fe-legend-dot" style="background:#667eea"></div>Category</div>
                    <div class="fe-legend-item"><div class="fe-legend-dot" style="background:#f59e0b"></div>Ideas Board</div>
                    <div class="fe-legend-item"><div class="fe-legend-dot" style="background:#10b981"></div>Discussion Forum</div>
                    <div class="fe-legend-item"><div class="fe-legend-dot" style="background:#ec4899"></div>Blog</div>
                    <div class="fe-legend-item"><div class="fe-legend-dot" style="background:#6366f1"></div>Knowledge Base</div>
                </div>
                <div id="fe-detail">
                    <button id="fe-detail-close">×</button>
                    <h2 id="fe-detail-title"></h2>
                    <div id="fe-detail-content"></div>
                    <div id="fe-messages"></div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);
    
    // Load D3 if needed
    if (!window.d3) {
        const s = document.createElement('script');
        s.src = 'https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js';
        document.head.appendChild(s);
        await new Promise(r => s.onload = r);
    }
    
    // Config
    const API = 'https://forums.autodesk.com/api/2.0';
    const COLORS = { category:'#667eea', idea:'#f59e0b', forum:'#10b981', blog:'#ec4899', tkb:'#6366f1', contest:'#8b5cf6', occasion:'#14b8a6', unknown:'#6b7280' };
    
    // State
    let allData = { categories: [], boards: [] };
    let filtered = { categories: [], boards: [] };
    let activeFilters = new Set(['category','idea','forum']);
    let simulation = null;
    
    const tooltip = document.getElementById('fe-tooltip');
    const detail = document.getElementById('fe-detail');
    
    // Handlers
    document.getElementById('fe-close').onclick = () => overlay.remove();
    document.getElementById('fe-detail-close').onclick = () => detail.classList.remove('visible');
    
    // Load data
    try {
        const catQ = encodeURIComponent("SELECT id,title,parent.id FROM nodes WHERE node_type='category' LIMIT 500");
        const catR = await fetch(API + '/search?q=' + catQ);
        const catD = await catR.json();
        
        const boardQ = encodeURIComponent("SELECT id,title,conversation_style,parent.id FROM nodes WHERE node_type='board' LIMIT 500");
        const boardR = await fetch(API + '/search?q=' + boardQ);
        const boardD = await boardR.json();
        
        allData.categories = (catD.data?.items || [])
            .map(c => ({ id: (c.id||'').replace('category:',''), title: c.title, type:'category', parent: c.parent?.id?.replace('category:','') }))
            .filter(c => !c.title.includes('Read Only') && !c.title.includes('Read-Only') && !c.title.includes('Archived') && c.id !== 'Archived');
        
        allData.boards = (boardD.data?.items || [])
            .map(b => ({ id: (b.id||'').replace('board:',''), title: b.title, type: b.conversation_style||'unknown', parent: b.parent?.id?.replace('category:','') }))
            .filter(b => !b.title.includes('Read Only') && !b.title.includes('Read-Only') && !b.title.includes('Archived'));
        
        filtered = JSON.parse(JSON.stringify(allData));
        console.log('Forum Explorer: Loaded', allData.categories.length, 'categories,', allData.boards.length, 'boards');
    } catch(err) {
        document.getElementById('fe-loading').innerHTML = '<div style="color:#ef4444">Error loading data: ' + err.message + '</div>';
        return;
    }
    
    // Setup filters
    const types = ['category', ...new Set(allData.boards.map(b => b.type))];
    const filterDiv = document.getElementById('fe-filters');
    types.forEach(type => {
        const count = type === 'category' ? allData.categories.length : allData.boards.filter(b => b.type === type).length;
        const label = document.createElement('label');
        label.className = 'fe-checkbox-item';
        label.innerHTML = '<input type="checkbox" value="'+type+'" '+(activeFilters.has(type)?'checked':'')+'><div class="fe-dot" style="background:'+(COLORS[type]||COLORS.unknown)+'"></div><span>'+type+' ('+count+')</span>';
        label.querySelector('input').onchange = (e) => {
            if (e.target.checked) activeFilters.add(type);
            else activeFilters.delete(type);
            applyFilters();
        };
        filterDiv.appendChild(label);
    });
    
    document.getElementById('fe-search').oninput = applyFilters;
    
    function applyFilters() {
        const s = document.getElementById('fe-search').value.toLowerCase();
        filtered.categories = allData.categories.filter(c => activeFilters.has('category') && c.title.toLowerCase().includes(s));
        filtered.boards = allData.boards.filter(b => activeFilters.has(b.type) && b.title.toLowerCase().includes(s));
        updateStats();
        renderList();
        renderGraph();
    }
    
    function updateStats() {
        document.getElementById('fe-stat-cat').textContent = filtered.categories.length;
        document.getElementById('fe-stat-board').textContent = filtered.boards.length;
        document.getElementById('fe-stat-idea').textContent = filtered.boards.filter(b => b.type === 'idea').length;
    }
    
    function renderList() {
        const c = document.getElementById('fe-list');
        c.innerHTML = '';
        const sorted = [...filtered.boards].sort((a,b) => {
            if (a.type === 'idea' && b.type !== 'idea') return -1;
            if (a.type !== 'idea' && b.type === 'idea') return 1;
            return a.title.localeCompare(b.title);
        });
        sorted.slice(0,100).forEach(board => {
            const item = document.createElement('div');
            item.className = 'fe-board-item';
            item.innerHTML = '<div class="fe-board-title">'+board.title+'</div><div class="fe-board-meta"><span class="fe-badge" style="background:'+(COLORS[board.type]||COLORS.unknown)+'20;color:'+(COLORS[board.type]||COLORS.unknown)+'">'+board.type+'</span>'+board.id+'</div>';
            item.onclick = () => selectBoard(board);
            c.appendChild(item);
        });
    }
    
    function renderGraph() {
        const container = document.getElementById('fe-graph-container');
        const width = container.clientWidth;
        const height = container.clientHeight;
        const svg = d3.select('#fe-graph');
        svg.selectAll('*').remove();
        
        const nodes = [];
        const links = [];
        const nodeMap = new Map();
        
        filtered.categories.forEach(cat => { nodes.push({...cat, nodeType:'category'}); nodeMap.set(cat.id, cat); });
        filtered.boards.forEach(board => {
            nodes.push({...board, nodeType:'board'});
            nodeMap.set(board.id, board);
            if (board.parent && nodeMap.has(board.parent)) links.push({source:board.parent, target:board.id});
        });
        filtered.categories.forEach(cat => {
            if (cat.parent && nodeMap.has(cat.parent)) links.push({source:cat.parent, target:cat.id});
        });
        
        if (!nodes.length) {
            svg.append('text').attr('x', width/2).attr('y', height/2).attr('text-anchor','middle').attr('fill','#666').text('No nodes match filters');
            return;
        }
        
        const g = svg.append('g');
        svg.call(d3.zoom().scaleExtent([0.1,4]).on('zoom', e => g.attr('transform', e.transform)));
        
        simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d=>d.id).distance(80))
            .force('charge', d3.forceManyBody().strength(-150))
            .force('center', d3.forceCenter(width/2, height/2))
            .force('collision', d3.forceCollide().radius(25));
        
        const link = g.append('g').selectAll('line').data(links).enter().append('line').attr('stroke','#2a2a3a').attr('stroke-width',1);
        
        const node = g.append('g').selectAll('g').data(nodes).enter().append('g').attr('cursor','pointer')
            .call(d3.drag()
                .on('start', (e,d) => { if(!e.active) simulation.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; })
                .on('drag', (e,d) => { d.fx=e.x; d.fy=e.y; })
                .on('end', (e,d) => { if(!e.active) simulation.alphaTarget(0); d.fx=null; d.fy=null; }));
        
        node.append('circle')
            .attr('r', d => d.nodeType==='category'?14:9)
            .attr('fill', d => COLORS[d.type]||COLORS.unknown)
            .attr('stroke','#1a1a25')
            .attr('stroke-width',2);
        
        node.filter(d => d.nodeType==='category' || d.type==='idea')
            .append('text')
            .attr('dx',15)
            .attr('dy',4)
            .attr('font-size','9px')
            .attr('fill','#777')
            .text(d => d.title.length>18?d.title.slice(0,18)+'...':d.title);
        
        node.on('mouseover', (e,d) => {
            tooltip.querySelector('h3').textContent = d.title;
            const url = d.nodeType === 'category' 
                ? 'https://forums.autodesk.com/t5/'+d.id+'/ct-p/'+d.id
                : 'https://forums.autodesk.com/t5/'+d.id+'/'+(d.type==='idea'?'idb':'bd')+'-p/'+d.id;
            tooltip.querySelector('#fe-tooltip-info').innerHTML = 'Type: '+(COLORS[d.type]?'<span style="color:'+COLORS[d.type]+'">'+d.type+'</span>':d.type)+'<br>ID: '+d.id+(d.parent?'<br>Parent: '+d.parent:'')+'<a href="'+url+'" target="_blank">Open in Forum →</a>';
            tooltip.style.left = (e.pageX+15)+'px';
            tooltip.style.top = (e.pageY+15)+'px';
            tooltip.classList.add('visible');
        })
        .on('mouseout', () => tooltip.classList.remove('visible'))
        .on('click', (e,d) => { if(d.nodeType==='board') selectBoard(d); });
        
        simulation.on('tick', () => {
            link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
            node.attr('transform', d => 'translate('+d.x+','+d.y+')');
        });
    }
    
    async function selectBoard(board) {
        // Highlight in list
        document.querySelectorAll('.fe-board-item').forEach(el => el.classList.remove('selected'));
        const items = document.querySelectorAll('.fe-board-item');
        items.forEach(el => { if (el.textContent.includes(board.id)) el.classList.add('selected'); });
        
        document.getElementById('fe-detail-title').textContent = board.title;
        document.getElementById('fe-detail-content').innerHTML = '<div style="color:#888;margin-bottom:15px">ID: '+board.id+'<br>Type: <span style="color:'+(COLORS[board.type]||COLORS.unknown)+'">'+board.type+'</span></div><h4 style="font-size:0.85rem;margin-bottom:10px">Top Posts by Kudos</h4>';
        const msgs = document.getElementById('fe-messages');
        msgs.innerHTML = '<div style="color:#666">Loading...</div>';
        detail.classList.add('visible');
        
        try {
            const q = encodeURIComponent("SELECT id,subject,kudos.sum(weight),metrics.views FROM messages WHERE board.id='"+board.id+"' AND depth=0 ORDER BY kudos.sum(weight) DESC LIMIT 10");
            const r = await fetch(API+'/search?q='+q);
            const d = await r.json();
            const items = d.data?.items || [];
            if (items.length) {
                msgs.innerHTML = items.map(m => '<div class="fe-message"><div class="fe-message-title">'+m.subject+'</div><div class="fe-message-stats">👍 '+(m.kudos?.sum?.weight||0)+' &nbsp; 👁️ '+(m.metrics?.views||0).toLocaleString()+'</div></div>').join('');
            } else {
                msgs.innerHTML = '<div style="color:#666">No messages found</div>';
            }
        } catch(err) {
            msgs.innerHTML = '<div style="color:#ef4444">Error loading messages</div>';
        }
    }
    
    // Initialize
    updateStats();
    renderList();
    renderGraph();
    document.getElementById('fe-loading').style.display = 'none';
    
    console.log('Forum Explorer ready!');
})();
