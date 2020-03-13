angular.module('costumer.app.static', [])
    .controller('CostumerController', ['$scope', '$http', CostumerController]);

function CostumerController($scope, $http) {
    $scope.costumers = [];
    $scope.costumer = {};
    $scope.errors = {};
    $scope.page = 1;
    $scope.orderBy = 'name';
    $scope.order = 'asc';
    $scope.search = '';
    $scope.totalRecords = 0;
    $scope.totalPages = 0;
    $scope.showStart = 1;
    $scope.showEnd = 10;
    $scope.nextPage = 2;
    $scope.previousPage = 1;
    $scope.sortIcon = {
        id: '',
        name: 'fa-sort-asc',
        city: '',
        age: ''
    }
    $scope.costumerUpdated = false;
    $scope.costumerDeleted = false;

    $scope.getCostumers = function (page = 1, orderBy = 'name', search = '', order = 'asc') {
        $scope.page = page;
        $scope.orderBy = orderBy;
        $scope.search = search;
        $scope.order = order;

        $http.get('/api/v1/costumer/?page=' + page + '&order_by=' + orderBy + '&search=' + search + '&order=' + order).then(function (res) {
            $scope.totalRecords = res.data.total_records;
            if (page > 1) {
                $scope.showStart = (page * 10) - 9;
                $scope.showEnd = (page * 10);
            } else {
                $scope.showStart = 1;
                if ($scope.totalRecords < 10) {
                    $scope.showEnd = $scope.totalRecords;
                } else {
                    $scope.showEnd = 10;
                }
            }
            if ($scope.showEnd > $scope.totalRecords) {
                $scope.showEnd = $scope.totalRecords;
            }
            $scope.totalPages = res.data.total_pages;
            if (page >= $scope.totalPages) {
                $scope.nextPage = page;
            } else {
                $scope.nextPage = page + 1;
            }
            if (page == 1) {
                $scope.previousPage = page;
            } else {
                $scope.previousPage = page - 1;
            }
            $scope.costumers = res.data.data;
        });
    };
    $scope.getCostumers();

    $scope.sortColumn = function (column) {
        if ($scope.orderBy == column) {
            if ($scope.order == 'asc') {
                $scope.order = 'desc';

            } else {
                $scope.order = 'asc'
            }
        } else {
            $scope.order = 'asc'
        }
        $scope.orderBy = column;
        $scope.sortIcon = {
            id: '',
            name: '',
            city: '',
            age: ''
        }
        $scope.sortIcon[column] = 'fa-sort-' + $scope.order;
        $scope.getCostumers($scope.page, column, $scope.search, $scope.order);
    };

    $scope.searchCostumers = function (search) {
        $scope.getCostumers(1, $scope.orderBy, search, $scope.order);
    };

    $scope.goNextPage = function (page) {
        $scope.getCostumers(page, $scope.orderBy, $scope.search, $scope.order);
    };

    $scope.goPreviousPage = function (page) {
        $scope.getCostumers(page, $scope.orderBy, $scope.search, $scope.order);
    };

    $scope.getCostumer = function (id) {
        $http.get('/api/v1/costumer/' + id).then(function (res) {
            $scope.costumer = res.data;
        });
    };

    $scope.cleanCostumer = function () {
        $scope.costumer = {};
        $scope.errors = {};
    };

    $scope.saveCostumer = function (costumer) {
        if (costumer.id) {
            $http.put('/api/v1/costumer/' + costumer.id + '/', costumer).then(function (res) {
                $scope.getCostumers();
                $scope.errors = {};
                $('.modal').modal('hide');
                $scope.costumerUpdated = true;
            }, function errorCallback(res) {
                if (res) {
                    $scope.errors = res.data;
                }
            });
        } else {
            $http.post('/api/v1/costumer/', costumer).then(function (res) {
                $scope.getCostumers();
                $scope.errors = {};
                $('.modal').modal('hide');
                $scope.costumerUpdated = true;
            }, function errorCallback(res) {
                if (res) {
                    $scope.errors = res.data;
                }
            });
        }
    };

    $scope.deleteCostumer = function (costumer) {
        $http.delete('/api/v1/costumer/' + costumer.id + '/').then(function (res) {
            $scope.getCostumers();
            $scope.errors = {};
            $scope.cleanCostumer();
            $('.modal').modal('hide');
            $scope.costumerDeleted = true;
        }, function errorCallback(res) {
            if (res) {
                $scope.errors = res.data;
            }
        });
    };

    $scope.closeAlert = function () {
        $scope.costumerDeleted = false;
        $scope.costumerUpdated = false;
    }

}
