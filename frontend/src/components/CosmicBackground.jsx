import React, { useEffect, useRef } from 'react';
import './cosmic.css';

export default function CosmicBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    // More stars with varying sizes and brightness
    const stars = Array.from({ length: Math.floor((w * h) / 5000) }).map(() => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 2 + 0.1,
      vx: (Math.random() - 0.5) * 0.08,
      vy: (Math.random() - 0.5) * 0.08,
      alpha: Math.random() * 0.9 + 0.1,
      twinkleSpeed: Math.random() * 0.02 + 0.01,
      color: ['#ffffff', '#88ccff', '#ffaaff', '#ffff88'][Math.floor(Math.random() * 4)],
      originalAlpha: Math.random() * 0.9 + 0.1,
    }));

    function resize() {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resize);

    let raf;
    let time = 0;
    function draw() {
      time += 0.016;
      ctx.clearRect(0, 0, w, h);

      // Complex nebula gradient with more colors
      const grad = ctx.createLinearGradient(0, 0, w, h);
      grad.addColorStop(0, 'rgba(6,8,25,0.8)');
      grad.addColorStop(0.3, 'rgba(30,10,60,0.4)');
      grad.addColorStop(0.5, 'rgba(10,25,50,0.3)');
      grad.addColorStop(0.7, 'rgba(40,15,70,0.35)');
      grad.addColorStop(1, 'rgba(5,10,30,0.7)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      // Draw radial nebula halos
      const nebGrad1 = ctx.createRadialGradient(w * 0.2, h * 0.3, 0, w * 0.2, h * 0.3, 400);
      nebGrad1.addColorStop(0, 'rgba(100,50,255,0.08)');
      nebGrad1.addColorStop(1, 'rgba(100,50,255,0)');
      ctx.fillStyle = nebGrad1;
      ctx.fillRect(0, 0, w, h);

      const nebGrad2 = ctx.createRadialGradient(w * 0.8, h * 0.7, 0, w * 0.8, h * 0.7, 350);
      nebGrad2.addColorStop(0, 'rgba(50,100,255,0.06)');
      nebGrad2.addColorStop(1, 'rgba(50,100,255,0)');
      ctx.fillStyle = nebGrad2;
      ctx.fillRect(0, 0, w, h);

      // Draw animated stars with twinkling
      for (let s of stars) {
        s.x += s.vx;
        s.y += s.vy;
        if (s.x < 0) s.x = w;
        if (s.x > w) s.x = 0;
        if (s.y < 0) s.y = h;
        if (s.y > h) s.y = 0;

        // Twinkling effect
        s.alpha = s.originalAlpha + Math.sin(time * s.twinkleSpeed) * 0.3;

        ctx.beginPath();
        ctx.globalAlpha = Math.max(0.1, s.alpha);
        ctx.fillStyle = s.color;
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();

        // Glow around bright stars
        if (s.r > 1) {
          ctx.globalAlpha = s.alpha * 0.3;
          ctx.fillStyle = s.color;
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r * 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      ctx.globalAlpha = 1;

      raf = requestAnimationFrame(draw);
    }

    draw();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <div className="cosmic-wrapper pointer-events-none">
      <div className="aurora" aria-hidden />
      <div className="nebula nebula-1" aria-hidden />
      <div className="nebula nebula-2" aria-hidden />
      
      <canvas ref={canvasRef} className="cosmic-canvas" />

      <div className="planet planet-1" aria-hidden />
      <div className="planet planet-2" aria-hidden />
      <div className="comet" aria-hidden />
    </div>
  );
}
