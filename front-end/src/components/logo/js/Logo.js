import * as createjs from 'createjs-module';

export default (state, stage, color, angleOffset) => {

	const shape = new createjs.Shape();
    const graphics = shape.graphics;
    stage.addChild(shape);

    shape.alpha = .5;

    const speed = 0.05;
    const certer = { x: state.width/2, y: state.height/2 };
    let angle = angleOffset;
    const rad = getRandom(1, 2);
    const radXOffset = getRandom(1, 6);
    const radYOffset = getRandom(1, 4);

	function draw() {
        graphics.clear().beginFill(color).drawCircle(certer.x, certer.y, 40);

        certer.x = rad * radXOffset * Math.cos( angle * speed ) + state.width/2
        certer.y = rad * radYOffset * 2 * Math.sin( angle * speed ) + state.height/2

        angle++;
    }

    function getRandom(min, max) {
        return Math.random() * (max - min) + min;
    }

    return {
        draw: draw
    }
}