var uoSuitsApp = angular.module('uoSuitsApp', ['angularMoment']);

uoSuitsApp.controller('SearchController', function($scope, $http, moment) {
  var searchUrl = 'https://search-uosuits-zf2mqzjundzog3jg2xjzuqeaye.us-west-2.es.amazonaws.com/uosuits/_search?q=';

  $scope.results = [];

  var itemResists = [
    'Cold Resist',
    'Energy Resist',
    'Fire Resist',
    'Physical Resist',
    'Poison Resist'
  ];

  $http
    .get(searchUrl + '*', {responseType:'json'})
    .then(function(result) {

      $scope.results = _.map(result.data.hits.hits, function(hit) {
        hit._source.names = _.join(hit._source.names, ',');
        
        hit._source.suits = _.sortBy(hit._source.suits, function(suit) {
          var date = moment(suit.found_date, 'YYYY-MM-DD:HH:mm:ss').format("YYYYMMDD");
          return date; 
        });
        
        return hit; 
      });

      calculateResists();

    })
    .catch(function(error) {
      console.log(error);  
    });

    // No way, way too ugly. Doing this in the import script
    var calculateResists = function() {
      _.forEach($scope.results, function(result) {
        var resists = {};
        _.forEach(result._source.suits[0].gear, function(gear) {
          _.forEach(gear.properties, function(property) {
            _.forEach(itemResists, function(resist) {
              if (_.startsWith(property, resist)) {
               
                
              }
            });          
          });
        });
      });
    };
});
