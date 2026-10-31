'use client';
import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    fetch('/empire.html')
      .then(r => r.text())
      .then(html => {
        document.documentElement.innerHTML = html;
      })
      .catch(() => {
        document.body.innerHTML = '<h1 style="color:white; text-align:center; margin-top:50vh;">Empire loading...</h1>';
      });
  }, []);

  return <div />;
}
