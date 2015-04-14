$(function () {
    window.player = new Board($('#board'));
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

function Player() {
    this.hand = [];
    this.columns = [];
}

Player.prototype.reset = function () {
   this.hand = [];
   this.columns = []
}

Player.prototype.draw = function (pile) {
    if(pile == "tactics") {
        if(tactics.cards.length == 0)
            alert("Tactics are drawn out, cannot draw any more.");
        else
            this.hand.push(tactics.cards.pop());
    }
    else {
        if(troops.cards.length == 0)
            alert("Troops are drawn out, cannot draw any more.");
        else
            this.hand.push(troops.cards.pop());
    }
}

Player.prototype.play = function (card, target) {

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