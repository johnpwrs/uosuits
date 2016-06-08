uoSuitsApp.controller('SearchController', 
  function($scope, $http, moment, $q, $location, $routeParams, 
    itemResists, skills, magicProperties, defenseProperties, regenProperties, 
    statProperties, attackProperties, properties, ignorePieces) {

  $scope.query = $routeParams.query;
  $scope.itemResists = itemResists;
  $scope.skills = skills;
  $scope.magicProperties = magicProperties;
  $scope.defenseProperties = defenseProperties;
  $scope.regenProperties = regenProperties;
  $scope.statProperties = statProperties;
  $scope.attackProperties = attackProperties;
  
  var searchUrl = '/search/';

  $scope.results = [];

  $scope.keys = _.keys;

  $scope.isSkill = function(prop) {
    return skills.indexOf(prop) > -1;
  };

  $scope.isResist = function(prop) {
    return itemResists.indexOf(prop) > -1;
  };

  $scope.ignorePiece = function(name) {
    return ignorePieces.indexOf(name) > -1;
  };

  $scope.goSearch = function() {
    var searchWord = $scope.searchWord || "*";
    $location.path('/search/' + searchWord);
  };

  $scope.loading = false;

  var from = 0;
  var done = false;

  $scope.scrollSearch = function() {
    if ($scope.results.length > 9 && !done) {
      from = from + 10;
      $scope.search($scope.searchWord, true);
    }
  };

  $scope.showTotal = false;

  $scope.search = function(searchWord, isScroll) {
    $scope.loading = true;
    searchWord = searchWord || $scope.searchWord || '*';
  
      $http
        .get(searchUrl + encodeURIComponent(searchWord) + "?from=" + from, 
          {responseType:'json'}
        )
      .then(function(result) {
        if (isScroll) {
          if (result.data.hits.hits.length < 1) {
            done = true;
          }
          $scope.results = _.union($scope.results, _.map(result.data.hits.hits, function(hit) {
            hit._source.suits = hit.inner_hits.suits.hits.hits[0]._source;
            hit._source.totalSuits = hit.inner_hits.suits.hits.total;
            return hit;
          }));

        }
        else {
          $scope.total = result.data.hits.total;
          $scope.results = _.map(result.data.hits.hits, function(hit) {
            hit._source.suits = hit.inner_hits.suits.hits.hits[0]._source;
            hit._source.totalSuits = hit.inner_hits.suits.hits.total;
            return hit;
          });
        }
        $scope.showTotal = true;
        $scope.loading = false;
      })
      .catch(function(error) {
        $scope.loading = false;
        console.log(error);  
      });

  };

  if ($scope.query) {
    $scope.search($scope.query);
    $scope.searchWord = $scope.query;
  }

//  $scope.search('*');

});
