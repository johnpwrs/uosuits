uoSuitsApp.controller('UserController', 
  function($scope, $http, moment, $routeParams, $sce, 
    itemResists, skills, magicProperties, defenseProperties, regenProperties, 
    statProperties, attackProperties, properties, ignorePieces) {
  
  $scope.userId = $routeParams.userId;
  $scope.itemResists = itemResists;
  $scope.skills = skills;
  $scope.magicProperties = magicProperties;
  $scope.defenseProperties = defenseProperties;
  $scope.regenProperties = regenProperties;
  $scope.statProperties = statProperties;
  $scope.attackProperties = attackProperties;

  $scope.hide = function(suit) {
    console.log("HERE");
    if (suit.show) {
      suit.show = false;
    }
    else {
      suit.show = true;
    }
  };
  

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

  $scope.ignoreItem = function(gear) {
    var ignore = false;
    _.forEach(ignorePieces, function(piece) {
      if (gear.src.indexOf(piece) > -1) {
        ignore = true;
        return;
      }
    });

    return ignore;
  };
 
  $scope.formatGear = function(gear) {
    //result = '<i class="fa-li fa fa-black-tie"></i>';
    result = '';
    splitGear = gear.src.split("$");
    var startingIndex = 0;

    if (gear.id) {
      startingIndex = 1;
    }
    
    for (var i = startingIndex; i < splitGear.length; i++) {
      if(i === startingIndex) {
        result += '<strong>' + splitGear[i] + '</strong>' + '<br>'; 
      }
      else {
        result += splitGear[i] + '<br>';
      }
    }
   
    return $sce.trustAsHtml(result); 
  };
 
  $scope.loading = false;
  
  var getUser = function(userId) {
    $scope.loading = true;
    $http
      .get('/user/' + encodeURIComponent(userId), {responseType:'json'})
      .then(function(result) {
        $scope.userResult = _.map(result.data.hits.hits, function(hit) {
          hit._source.suits = hit.inner_hits.suits.hits.hits;
          return hit;
        })[0];
        $scope.loading = false;

        console.log($scope.userResult);
      })
      .catch(function(error) {
        $scope.loading = false;
        console.log(error);  
      });
  };

  getUser($scope.userId);
});
