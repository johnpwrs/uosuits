var uoSuitsApp = angular.module('uoSuitsApp', 
    ['angularMoment', 'ngRoute', 'infinite-scroll', 'angular-timeline']
  )
  .filter('date', function() {
    return function(input) {
      return moment(input, 'YYYY-MM-DDTHH:mm:ssZ').format("MMM D, YYYY @ h:mma");
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
        .when('/search/:query', {
          templateUrl: '/views/search_results.html',
          controller: 'SearchController'  
        })
        .otherwise({
          templateUrl: '/views/main_search.html',
          controller: 'SearchController'
        });
    }
  ])
  .constant('itemResists', [
    'Physical Resist',
    'Fire Resist',
    'Cold Resist',
    'Poison Resist',
    'Energy Resist'
  ])
  .constant('skills', [
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
 ])
 .constant('magicProperties', [
    'Enhance Potions',
    'Faster Cast Recovery',
    'Faster Casting',
    'Spell Damage Increase',
    'Lower Mana Cost',
    'Lower Reagent Cost',
    'Casting Focus',
    'Mana Burst',
    'Mana Phase'
  ])
  .constant('defenseProperties', [
    'Defense Chance Increase',
    'Reflect Physical Damage',
    'Damage Eater',
    'Poison Eater',
    'Fire Eater',
    'Energy Eater',
    'Kinetic Eater',
    'Cold Eater',
    'Reactive Paralyze'
  ])
  .constant('regenProperties', [
    'Mana Regeneration',
    'Hit Point Regeneration',
    'Stamina Regeneration'
  ])
  .constant('statProperties', [
    'Mana Increase',
    'Hit Point Increase',
    'Stamina Increase',
    'Intelligence Bonus',
    'Dexterity Bonus',
    'Strength Bonus'
  ])
  .constant('attackProperties', [
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
  ])
  .constant('properties', [
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
  ])
  .constant('ignorePieces', [
    'Tiller', 
    'Ponytail', 
    'Ship', 
    'Backpack', 
    'Long Hair', 
    'Long Beard', 
    'Mustache'
  ]);

