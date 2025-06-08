// importするカメラハンドラークラス
export class CameraHandler {
    constructor(videoElementId, canvasElementId, imageElementId) {
        this.videoElement = document.getElementById(videoElementId);
        this.canvasElement = document.getElementById(canvasElementId);
        this.imageElement = document.getElementById(imageElementId);
        this.cameraRunning = false
    }

    // カメラを起動するメソッド
    startCamera() {
        console.log("startCamera")
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                this.stream = stream;
                this.videoElement.srcObject = stream;
                this.videoElement.style.transform = 'scaleX(-1)'; // 左右反転
            })
            .catch(err => {
                console.error("Error accessing camera: ", err);
            });
        this.cameraRunning = true
    }

    // カメラを停止するメソッド
    stopCamera() {
        console.log("stopCamera")
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop()); // ストリームのトラックを停止
            this.stream = null; // ストリームのリセット
            this.videoElement.srcObject = null; // ビデオ要素のsrcObjectをクリア
            this.cameraRunning = false
        }
    }

    // 撮影するメソッド
    captureImage() {
        const context = this.canvasElement.getContext('2d');
        context.scale(-1, 1); // 水平方向に反転
        context.drawImage(this.videoElement, 0, 0, -this.canvasElement.width, this.canvasElement.height);
        const dataUrl = this.canvasElement.toDataURL('image/png');
        this.imageElement.src = dataUrl;
        this.imageElement.style.display = 'block';
        return dataUrl;
    }
}
