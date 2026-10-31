'use client';
import { useEffect } from 'react';

export default function EmpirePage() {
  useEffect(() => {
    // Load and inject the HTML
    fetch('/empire.html')
      .then(r => r.text())
      .then(html => {
        document.documentElement.innerHTML = html;
      });
  }, []);

  return <div />;
}
