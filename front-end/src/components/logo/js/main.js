import SceneManager from "./SceneManager"

export default container => {

    const canvas = createCanvas(document, container);

    window.onresize = resizeCanvas;

    const sceneManager = new SceneManager(canvas);

    resizeCanvas();
    render();

    function render() {
        requestAnimationFrame(render);
        sceneManager.update();
    }

    function createCanvas(document, container) {
        const canvas = document.createElement('canvas');     
        container.appendChild(canvas);
        return canvas;
    }

    function resizeCanvas() {        
        canvas.style.width = '100%';
        canvas.style.height= '100%';
        
        canvas.width  = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        sceneManager.onWindowResize()
        sceneManager.update()
    }
}