self.addEventListener('message', function(e) {
    importScripts('md5.min.js');
    var symbols = "abcdefghijklmnopqrstuvwxyz".split("");
    symbols.push("", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9");
    pass = '';
    for (i = 0; i < symbols.length; i++){
        for (j = 0; j < symbols.length; j++){
            for (k = 0; k < symbols.length; k++){
                for (m = 0; m < symbols.length; m++){
                    var pass = symbols[i] + symbols[j] + symbols[k] + symbols[m];
                    var hash = md5(pass);
                    if (hash == e.data[0])
                        self.postMessage(pass);
                }
            }
        }
    }
    self.postMessage(0);
}, false);