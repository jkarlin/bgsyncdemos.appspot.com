self.addEventListener('sync', function(event) {
    caches.open("outbox")
        .then( function (cache) {
            return cache.match(new Request("to_post"))
                .then( function (response) {
                    return cache.delete(new Request("to_post"))
                        .then(function () {
                            return response.text();
                        })
                });
        })
        .then( function (msg) {
            return fetch(new Request("post", {
                method: "post",
                headers: { "Content-Type": "application/json;charset=UTF-8" },
                body: JSON.stringify({text: msg})
            }))
        })
        .then( function (response) {
            return response.text();
        })
        .then ( function (txt) {
            console.log("sw Response: " + txt);
        })
});