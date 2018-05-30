navigator.serviceWorker && navigator.serviceWorker.register('/static/js/sw.js').then(function(registration) {
  console.log('Excellent, registered with scope: ', registration.scope);
});

navigator.serviceWorker && navigator.serviceWorker.ready.then(function(serviceWorkerRegistration) {
  serviceWorkerRegistration.pushManager.getSubscription()
    .then(function(subscription) {
if (subscription) {
        console.info('Got existing', subscription);
        window.subscription = subscription;
        return;  // got one, yay
      }

      const publicKey = 'BCSJ-hbPDIFucPJ7BKS0BrBz_4Cv96IVpAqsjTuiSgIXByB6hlcvTD53G3Q8EMayzfbVqS7Gg7Q2mPLTeQvTvCo';
      const applicationServerKey = urlB64ToUint8Array(publicKey);
      serviceWorkerRegistration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey,
      })
        .then(function(subscription) {
          console.info('Newly subscribed to push!', subscription);
          window.subscription = subscription;
        });
    });
});