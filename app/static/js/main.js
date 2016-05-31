var uoSuitsApp = angular.module('uoSuitsApp', ['angularMoment', 'ngRoute'])
  .filter('date', function() {
    return function(input) {
      return moment(input, 'YYYY-MM-DDTHH:mm:ssZ').format("MMM D, YYYY @ h:ma");
    };
  })
  .filter('names', function() {
    return function(input) {
      return _.join(input, ', '); 
    };
  })
  .config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
      $routeProvider
        .when('/user/:userId', {
          templateUrl: '/views/user_detail.html',
          controller: 'UserController'
        })
        .when('/', {
          templateUrl: '/views/main_search.html',
          controller: 'SearchController'
        });
    }
  ]);

uoSuitsApp.controller('UserController', function($scope, $http, moment, $routeParams, $sce) {
  $scope.userId = $routeParams.userId;
  
  $scope.itemResists = [
    'Physical Resist',
    'Fire Resist',
    'Cold Resist',
    'Poison Resist',
    'Energy Resist'
  ];

  $scope.skills = [
    'Archery',
    'Chivalry',
    'Fencing',
    'Focus',
    'Mace Fighting',
    'Parrying',
    'Swordsmanship',
    'Tactics',
    'Wrestling',
    'Bushido',
    'Throwing',
    'Healing',
    'Veterinary',
    'Alchemy',
    'Evaluating Intelligence',
    'Evaluate Intelligence',
    'Inscription',
    'Magery',
    'Meditation',
    'Necromancy',
    'Resisting Spells',
    'Spellweaving',
    'Spirit Speak',
    'Mysticism',
    'Discordance',
    'Musicianship',
    'Peacemaking',
    'Provocation',
    'Begging',
    'Detecting Hidden',
    'Hiding',
    'Lockpicking',
    'Poisoning',
    'Remove Trap',
    'Snooping',
    'Stealing',
    'Stealth',
    'Ninjitsu',
    'Anatomy',
    'Animal Lore',
    'Animal Taming',
    'Camping',
    'Forensic Evaluation',
    'Herding',
    'Taste Identification',
    'Tracking',
    'Arms Lore',
    'Blacksmith',
    'Carpentry',
    'Cooking',
    'Item Identification',
    'Tailoring',
    'Tinkering',
    'Imbuing',
    'Fishing',
    'Mining',
    'Lumberjacking'
  ];

  $scope.magicProperties = [
    'Enhance Potions',
    'Faster Cast Recovery',
    'Faster Casting',
    'Spell Damage Increase',
    'Lower Mana Cost',
    'Lower Reagent Cost',
    'Casting Focus',
    'Mana Burst',
    'Mana Phase'
  ];

  $scope.defenseProperties = [
    'Defense Chance Increase',
    'Reflect Physical Damage',
    'Damage Eater',
    'Poison Eater',
    'Fire Eater',
    'Energy Eater',
    'Kinetic Eater',
    'Cold Eater',
    'Reactive Paralyze'
  ];

  $scope.regenProperties = [
    'Mana Regeneration',
    'Hit Point Regeneration',
    'Stamina Regeneration'
  ];

  $scope.statProperties = [
    'Mana Increase',
    'Hit Point Increase',
    'Stamina Increase',
    'Intelligence Bonus',
    'Dexterity Bonus',
    'Strength Bonus'
  ];

  $scope.attackProperties = [
    'Hit Chance Increase',
    'Damage Increase',
    'Physical Damage',
    'Damage Modifier',
    'Fire Damage',
    'Poison Damage',
    'Cold Damage',
    'Energy Damage',
    'Chaos Damage',
    'Swing Speed Increase',
    'Velocity',
    'Hit Cold Area',
    'Hit Energy Area',
    'Hit Fire Area',
    'Hit Physical Area',
    'Hit Poison Area',
    'Hit Curse',
    'Hit Dispel',
    'Hit Fatigue',
    'Hit Fireball',
    'Hit Harm',
    'Hit Life Leech',
    'Hit Lightning',
    'Hit Lower Attack',
    'Hit Lower Defense',
    'Hit Mana Drain',
    'Hit Mana Leech',
    'Hit Stamina Leech'
  ];

  var properties = [
    'Lower Requirements',
    'Luck',
    'Skill Bonus',
    'Blood Drinker',
    'Battle Lust',
    'Resonance',
    'Soul Charge',
    'Splintering Weapon',
    'Bane',
    'Increased Karma Loss',
    'Lifespan',
    'Lower Ammo Cost',
    'Rage Focus',
    'Weight Reduction'
  ];

  var ignorePieces = ['Tiller', 'Ponytail', 'Ship', 'Backpack', 'Long Hair', 'Long Beard', 'Mustache'];

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
    result = '<i class="fa-li fa fa-black-tie"></i>';
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
  
  var getUser = function(userId) {
    $http
      .get('/user/' + encodeURIComponent(userId), {responseType:'json'})
      .then(function(result) {
        $scope.userResult = _.map(result.data.hits.hits, function(hit) {
          hit._source.suits = hit.inner_hits.suits.hits.hits;
          return hit;
        })[0];

        console.log($scope.userResult);
      })
      .catch(function(error) {
        console.log(error);  
      });
  };

  getUser($scope.userId);
});

uoSuitsApp.controller('SearchController', function($scope, $http, moment) {
  var searchUrl = '/search/';
  $scope.results = [];

  $scope.itemResists = [
    'Physical Resist',
    'Fire Resist',
    'Cold Resist',
    'Poison Resist',
    'Energy Resist'
  ];

  $scope.skills = [
    'Archery',
    'Chivalry',
    'Fencing',
    'Focus',
    'Mace Fighting',
    'Parrying',
    'Swordsmanship',
    'Tactics',
    'Wrestling',
    'Bushido',
    'Throwing',
    'Healing',
    'Veterinary',
    'Alchemy',
    'Evaluating Intelligence',
    'Evaluate Intelligence',
    'Inscription',
    'Magery',
    'Meditation',
    'Necromancy',
    'Resisting Spells',
    'Spellweaving',
    'Spirit Speak',
    'Mysticism',
    'Discordance',
    'Musicianship',
    'Peacemaking',
    'Provocation',
    'Begging',
    'Detecting Hidden',
    'Hiding',
    'Lockpicking',
    'Poisoning',
    'Remove Trap',
    'Snooping',
    'Stealing',
    'Stealth',
    'Ninjitsu',
    'Anatomy',
    'Animal Lore',
    'Animal Taming',
    'Camping',
    'Forensic Evaluation',
    'Herding',
    'Taste Identification',
    'Tracking',
    'Arms Lore',
    'Blacksmith',
    'Carpentry',
    'Cooking',
    'Item Identification',
    'Tailoring',
    'Tinkering',
    'Imbuing',
    'Fishing',
    'Mining',
    'Lumberjacking'
  ];

  $scope.magicProperties = [
    'Enhance Potions',
    'Faster Cast Recovery',
    'Faster Casting',
    'Spell Damage Increase',
    'Lower Mana Cost',
    'Lower Reagent Cost',
    'Casting Focus',
    'Mana Burst',
    'Mana Phase'
  ];

  $scope.defenseProperties = [
    'Defense Chance Increase',
    'Reflect Physical Damage',
    'Damage Eater',
    'Poison Eater',
    'Fire Eater',
    'Energy Eater',
    'Kinetic Eater',
    'Cold Eater',
    'Reactive Paralyze'
  ];

  $scope.regenProperties = [
    'Mana Regeneration',
    'Hit Point Regeneration',
    'Stamina Regeneration'
  ];

  $scope.statProperties = [
    'Mana Increase',
    'Hit Point Increase',
    'Stamina Increase',
    'Intelligence Bonus',
    'Dexterity Bonus',
    'Strength Bonus'
  ];

  $scope.attackProperties = [
    'Hit Chance Increase',
    'Damage Increase',
    'Physical Damage',
    'Damage Modifier',
    'Fire Damage',
    'Poison Damage',
    'Cold Damage',
    'Energy Damage',
    'Chaos Damage',
    'Swing Speed Increase',
    'Velocity',
    'Hit Cold Area',
    'Hit Energy Area',
    'Hit Fire Area',
    'Hit Physical Area',
    'Hit Poison Area',
    'Hit Curse',
    'Hit Dispel',
    'Hit Fatigue',
    'Hit Fireball',
    'Hit Harm',
    'Hit Life Leech',
    'Hit Lightning',
    'Hit Lower Attack',
    'Hit Lower Defense',
    'Hit Mana Drain',
    'Hit Mana Leech',
    'Hit Stamina Leech'
  ];

  var properties = [
    'Lower Requirements',
    'Luck',
    'Skill Bonus',
    'Blood Drinker',
    'Battle Lust',
    'Resonance',
    'Soul Charge',
    'Splintering Weapon',
    'Bane',
    'Increased Karma Loss',
    'Lifespan',
    'Lower Ammo Cost',
    'Rage Focus',
    'Weight Reduction'
  ];

  var ignorePieces = ['Tiller', 'Ponytail', 'Ship', 'Backpack', 'Long Hair', 'Long Beard', 'Mustache'];

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

  $scope.search = function(searchWord) {
    searchWord = searchWord || $scope.searchWord || '*';
    $http
      .get(searchUrl + encodeURIComponent(searchWord), {responseType:'json'})
      .then(function(result) {
        $scope.results = _.map(result.data.hits.hits, function(hit) {
          hit._source.suits = hit.inner_hits.suits.hits.hits[0]._source;
          hit._source.totalSuits = hit.inner_hits.suits.hits.total;
          return hit;
        });
      })
      .catch(function(error) {
        console.log(error);  
      });
  };

  $scope.search('*');

});
