import test from 'node:test';
import assert from 'node:assert/strict';
import { validateResponse } from '../app/revision-game.ts';
await test('numeric answers accept locale decimal separators and reject partial numbers',()=>{
 for(const value of ['12.5','12,5',' 12.50 ']) assert.ok(validateResponse('number','12.5',value));
 for(const value of ['12','12.5kg','12,5,0','','Infinity','1e1']) assert.equal(validateResponse('number','12.5',value),false);
});
await test('time answers accept keypad input without accepting invalid clock notation',()=>{
 for(const value of ['18:15','1815','18.15','18 15']) assert.ok(validateResponse('time','18:15',value));
 for(const value of ['1:81:5','18:05','17:75','24:00','18:150','']) assert.equal(validateResponse('time','18:15',value),false);
});
await test('ordering requires each card exactly once in the intended position',()=>{
 const expected=[2,0,1];
 for(const a of [0,1,2])for(const b of [0,1,2])for(const c of [0,1,2])assert.equal(validateResponse('order',expected,[a,b,c]),a===2&&b===0&&c===1);
 for(const value of [[],[2,0],[2,0,1,1]])assert.equal(validateResponse('order',expected,value),false);
});
await test('choice validation rejects missing and out-of-range choices',()=>{
 assert.ok(validateResponse('choice',1,'1'));
 for(const value of ['','0','2','1.0','one'])assert.equal(validateResponse('choice',1,value),false);
});
await test('multi-select answers require exactly the expected set in any order',()=>{
 const expected=[0,1,3];
 for(const value of [[0,1,3],[3,1,0],[1,3,0]]) assert.ok(validateResponse('multi',expected,value));
 for(const value of [[],[0,1],[0,1,2,3],[0,1,1,3],[2]]) assert.equal(validateResponse('multi',expected,value),false);
 assert.equal(validateResponse('multi',expected,'0,1,3'),false);
});
