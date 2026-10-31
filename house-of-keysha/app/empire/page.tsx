'use client';
export default function EmpirePage() {
  return (
    <div style={{width: '100%', height: '100vh', overflow: 'hidden'}}>
      <iframe
        srcDoc={require('fs').readFileSync('/home/userkeysha2000/house-of-keysha-empire/index.html', 'utf8')}
        style={{width: '100%', height: '100%', border: 'none'}}
        title="House of Keysha Empire"
      />
    </div>
  );
}
