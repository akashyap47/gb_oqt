var gbOqtApp = angular.module("gbOqtApp", []);

gbOqtApp.controller("LangCtrl", ["$scope", "$http", function($scope, $http) {
	$scope.setLang = function(lang) {
		$http.post("/set_lang/", {"lang": lang}).
		success(function(data, status, headers, config) {
			window.location = "http://localhost:5000/" + data["next"] + "/";
		}).
		error(function(data, status, headers, config) {
			$scope.setLang(lang);
		});
	}
}]);

gbOqtApp.controller("ConsentCtrl", ["$scope", "$http", function($scope, $http) {
	$scope.setConsent = function(consent) {
		$http.post("/set_consent/", {"consent": consent}).
		success(function(data, status, headers, config) {
			window.location = "http://localhost:5000/" + data["next"] + "/";
		}).
		error(function(data, status, headers, config) {
			$scope.setConsent();
		});
	}
}]);

gbOqtApp.controller("DemographicsCtrl", ["$scope", "$http", function($scope, $http) {
	$scope.demographics = {
		'age': 'na',
		'gender': 'na',
		'education': 'na',
		'country_origin': 'na',
		'country_residence': 'na',
		'native_lang': 'na'
	};

	$scope.setDemographics = function() {
		$http.post("/set_demographics/", $scope.demographics).
		success(function(data, status, headers, config) {
			window.location = "http://localhost:5000/" + data["next"] + "/";
		}).
		error(function(data, status, headers, config) {
			$scope.setDemographics();
		});
	}
}]);

gbOqtApp.controller("QuizCtrl", ["$scope", "$http", function($scope, $http) {
	$scope.quiz = {
		'q1_ans': 'na',
		'q2_ans': 'na',
		'q3_ans': 'na',
		'q4_ans': 'na',
		'q5_ans': 'na',
		'q6_ans': 'na',
		'q7_ans': 'na',
		'q8_ans': 'na',
		'q9_ans': 'na',
		'q10_ans': 'na',
		'q11_ans': 'na',
		'q12_ans': 'na',
		'q13_ans': 'na',
		'q14_ans': 'na',
		'q15_ans': 'na',
		'q16_ans': 'na',
		'q17_ans': 'na',
		'q18_ans': 'na',
		'q19_ans': 'na',
		'q20_ans': 'na',
		'q21_ans': 'na',
		'q22_ans': 'na'
	};

	$scope.submitQuiz = function() {
		console.log($scope.quiz)
		$http.post("/submit_quiz/", $scope.quiz).
		success(function(data, status, headers, config) {
			window.location = "http://localhost:5000/" + data["next"] + "/";
		}).
		error(function(data, status, headers, config) {
			$scope.submitQuiz();
		});
	}
}]);