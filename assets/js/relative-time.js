<script>
(function(){
  function humanizeKorean(dt){
    const now = new Date();
    const s = Math.floor((now - dt)/1000);
    if (s < 60) return '방금 전';
    const m = Math.floor(s/60);
    if (m < 60) return `${m}분 전`;
    const h = Math.floor(m/60);
    if (h < 24) return `${h}시간 전`;
    const d = Math.floor(h/24);
    if (d === 1) return '어제';
    if (d < 30) return `${d}일 전`;
    const mo = Math.floor(d/30);
    if (mo < 12) return `${mo}개월 전`;
    const y = Math.floor(mo/12);
    return `${y}년 전`;
  }

  function updateRel(){
    document.querySelectorAll('.wb-updated-rel[data-iso]').forEach(el=>{
      const iso = el.getAttribute('data-iso');
      const dt = new Date(iso);
      if (!isNaN(dt)) el.textContent = `(${humanizeKorean(dt)})`;
    });
  }

  // 초기 1회 + 1분마다 갱신
  updateRel();
  setInterval(updateRel, 60 * 1000);
})();
</script>
