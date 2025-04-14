self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open('pwa-cache').then(function(cache) {
      return cache.addAll([
        '/',
        '/static/icon/icon-192x192.png',
        '/static/icon/icon-512x512.png'
      ]);
    })
  );
});

self.addEventListener('fetch', function(e) {
  console.log('[ServiceWorker] Fetch', e.request.url);
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});