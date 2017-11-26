import * as createjs from 'createjs-module';
import Logo from "./Logo"

export default canvas => {
	
	const state = {
        pixelRatio: -1,

        width: -1,
        height: -1
    }

    const stage = new createjs.Stage(canvas);
    state.pixelRatio = getPixelRatio(canvas.getContext('2d'));

    const logoR = new Logo(state, stage, "#00FFFF", 0);
    const logoG = new Logo(state, stage, "#FF00FF", 180);
    const logoB = new Logo(state, stage, "#FFFF00", 360);

    function update() {
        logoR.draw();
        logoG.draw();
        logoB.draw();

        stage.update();
    }

    function onWindowResize() {
        var width = 100 * state.pixelRatio;
        var height =100 * state.pixelRatio;

        canvas.setAttribute('width', Math.round(width));
        canvas.setAttribute('height', Math.round(height));

        state.width = width;
        state.height = height;
    }

    function getPixelRatio(context) {
        const devicePixelRatio = window.devicePixelRatio || 1;
        const backingStoreRatio = context.webkitBackingStorePixelRatio ||
            context.mozBackingStorePixelRatio ||
            context.msBackingStorePixelRatio ||
            context.oBackingStorePixelRatio ||
            context.backingStorePixelRatio || 
            1;
    
        return devicePixelRatio / backingStoreRatio;
    }

    return {
        update,
        onWindowResize,
    }
}