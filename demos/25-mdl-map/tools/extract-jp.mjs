import fs from 'node:fs'; import * as topojson from 'topojson-client';
const [src,dst]=process.argv.slice(2); const topo=JSON.parse(fs.readFileSync(src,'utf8'));
const fc=topojson.feature(topo, topo.objects.countries); const jp=fc.features.find(f=>f.properties.name==='Japan');
// keep polygons as [ [ [lon,lat],... ] (outer ring) ], drop rings with tiny area
const polys=(jp.geometry.type==='Polygon'?[jp.geometry.coordinates]:jp.geometry.coordinates);
const area=r=>{let a=0;for(let i=0;i<r.length-1;i++)a+=r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1];return Math.abs(a/2);};
const keep=polys.map(p=>p[0]).filter(r=>area(r)>0.01).map(r=>r.map(([x,y])=>[+x.toFixed(4),+y.toFixed(4)]));
fs.writeFileSync(dst, JSON.stringify({source:'Natural Earth 1:10m via world-atlas@2.0.2 (public domain)',rings:keep}));
console.log('rings',keep.length,'points',keep.reduce((s,r)=>s+r.length,0), keep.map(r=>area(r).toFixed(2)).join(' '));
