// Installazione immediata
self.addEventListener("install", event => {
  self.skipWaiting();
});

// Attivazione immediata
self.addEventListener("activate", event => {
  clients.claim();
});

// Modalità sicura: NON intercetta le richieste
self.addEventListener("fetch", event => {
  // Non fare nulla, lascia tutto al server
});
