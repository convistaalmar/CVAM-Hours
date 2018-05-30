/** An empty service worker! */
self.addEventListener('fetch', function(event) {
  /** An empty fetch handler! */
});

self.addEventListener('push', function(event) {
  event.waitUntil(
    self.registration.showNotification('Got Push?', {
      body: 'Push Message received'
   }));
});