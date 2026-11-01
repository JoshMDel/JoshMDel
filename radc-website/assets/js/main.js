// Mobile navigation toggle
(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('site-nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});}
  // Booking form -> pre-filled WhatsApp message (no server required)
  var f=document.getElementById('booking-form');
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault();
    var v=function(id){var el=document.getElementById(id);return el&&el.value?el.value.trim():'';};
    var lines=["Hi RADC, I'd like a quote / booking."];
    if(v('bf-name'))lines.push('Name: '+v('bf-name'));
    if(v('bf-vehicle'))lines.push('Vehicle: '+v('bf-vehicle'));
    if(v('bf-service'))lines.push('Service: '+v('bf-service'));
    if(v('bf-town'))lines.push('Town: '+v('bf-town'));
    if(v('bf-date'))lines.push('Preferred date: '+v('bf-date'));
    if(v('bf-msg'))lines.push('Notes: '+v('bf-msg'));
    var url='https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(lines.join('\n'));
    if(window.gtag){gtag('event','generate_lead',{method:'whatsapp_form'});}
    window.open(url,'_blank','noopener');
  });}
  // Click tracking hooks for GA4 (only fires if gtag is installed)
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="tel:"],a[href*="wa.me"]');
    if(a&&window.gtag){gtag('event',a.href.indexOf('tel:')===0?'click_call':'click_whatsapp',{link_url:a.href});}
  });
})();
