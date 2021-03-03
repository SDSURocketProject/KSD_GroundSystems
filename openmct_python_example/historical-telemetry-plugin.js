/**
 * Basic historical telemetry plugin.
 */

function HistoricalTelemetryPlugin() {
    return function install (openmct) {
        var provider = {
            supportsRequest: function (domainObject) {
                return domainObject.type === 'example.telemetry';
            },
            request: function (domainObject, options) {                
                pythonUrl = 'http://localhost:8090/history/' +
                    domainObject.identifier.key +
                    '?start=' + options.start +
                    '&end=' + options.end;
                
                return fetch(pythonUrl).then(response => response.json())
            }
        };

        openmct.telemetry.addProvider(provider);
    }
}
