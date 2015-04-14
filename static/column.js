$(function () {
    window.troops = new Board($('#board'));
    gameboard.createNumHash();
    gameboard.reset();
    $('.cell').click(function (event) {

        if ($(this).html() == '') {
            $(this).html('X');
            gameboard.adjustSetCount('X', event.target.id);
            ai.play();
        }
    });
});

function Column() {
    this.size = 3;
}

//Troop inherits from card
function Troop(value, color) {
    Card.call(this);
    this.value = value;
    this.color = color;
}
Troop.prototype = Object.create(Card.prototype);

//Tactic inherits from card
function Tactic(ability) {
    this.ability = ability;
}
Tactic.prototype = Object.create(Card.prototype);

//Will maintain counts of each player's marks in each possible set of 3.
//Stored in $('#board').data
Card.prototype.value = 0; //all sets of 3
Board.prototype.numHash = {}; //to be a map of all sets in which a cell are included. e.g. 1-> 123, 147, 159, 2 -> 123, 258,

//clear board and all game-specific data
Board.prototype.reset = function () {

    $('.cell').html('');
    for (var i = 0; i < this.setsOfThree.length; i++) {
        this.board.data(this.setsOfThree[i], {'X': 0, 'O': 0});
    }
    this.board.data('numTurns', 0);

}

Board.prototype.adjustSetCount = function (player, cell) {
    //mapping increased count to each of the 3-sets that include played cell.
    for (var i = 0; i < this.numHash[cell].length; i++) {
        if (player == 'X') {
            this.board.data(this.numHash[cell][i])['X']++;
        }
        else {
            this.board.data(this.numHash[cell][i])['O']++;
        }
    }
    this.board.data().numTurns++;
    this.checkGameStatus();
}

//check for game-ending setups, e.g. two in a row with open third.
Board.prototype.hasTwoInRow = function (player) {
    for (var i = 0; i < this.setsOfThree.length; i++) {
        var currentSet = this.board.data(this.setsOfThree[i]);

        if (player == 'X') {
            //X has 2 in a 3-set, with the remaining cell open.
            if (currentSet['X'] == 2 && currentSet['O'] == 0)
                return this.setsOfThree[i];
        } else {
            if (currentSet['O'] == 2 && currentSet['X'] == 0)
                return this.setsOfThree[i];
        }

    }
    return null;
}

//check if any of our 8 sets are completed by a single player or all squares are full
Board.prototype.checkGameStatus = function () {
    for (var i = 0; i < this.setsOfThree.length; i++) {
        var currentSet = this.board.data(this.setsOfThree[i]);

        if (currentSet['X'] == 3) {
            alert("You win!");
            this.reset();
        }
        else if (currentSet['O'] == 3) {
            alert("Uh oh! Computer wins!");
            this.reset();
        }

    }

    if ($('#board').data('numTurns') == 9) {
        alert("Tie Game!");
        this.reset();
    }

}

//set up a map of all sets in which a cell are included. e.g. 1-> 123, 147, 159, 2 -> 123, 258
Board.prototype.createNumHash = function () {

    for (var i = 1; i < 10; i++) {
        this.numHash[i] = [];
        for (var j = 0; j < this.setsOfThree.length; j++) {
            if (this.setsOfThree[j].indexOf(i) > -1)
                this.numHash[i].push(this.setsOfThree[j]);
        }
    }
}