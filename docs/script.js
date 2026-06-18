// Computer Vision Application - Interactive Demo Script

document.addEventListener('DOMContentLoaded', function() {
    // Canvas elements
    const originalCanvas = document.getElementById('originalCanvas');
    const processedCanvas = document.getElementById('processedCanvas');
    const originalCtx = originalCanvas.getContext('2d');
    const processedCtx = processedCanvas.getContext('2d');
    
    // Control elements
    const operationSelect = document.getElementById('operationSelect');
    const kernelSizeInput = document.getElementById('kernelSize');
    const thresholdMinInput = document.getElementById('thresholdMin');
    const thresholdMaxInput = document.getElementById('thresholdMax');
    const kernelValue = document.getElementById('kernelValue');
    const minValue = document.getElementById('minValue');
    const maxValue = document.getElementById('maxValue');
    const applyBtn = document.getElementById('applyBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    // Set canvas size
    const canvasWidth = 400;
    const canvasHeight = 300;
    originalCanvas.width = canvasWidth;
    originalCanvas.height = canvasHeight;
    processedCanvas.width = canvasWidth;
    processedCanvas.height = canvasHeight;
    
    // Sample image data (simple gradient pattern)
    let imageData = null;
    
    // Create sample image
    function createSampleImage() {
        const imgData = originalCtx.createImageData(canvasWidth, canvasHeight);
        const data = imgData.data;
        
        for (let y = 0; y < canvasHeight; y++) {
            for (let x = 0; x < canvasWidth; x++) {
                const idx = (y * canvasWidth + x) * 4;
                
                // Create a pattern with shapes
                const centerX = canvasWidth / 2;
                const centerY = canvasHeight / 2;
                const distFromCenter = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
                
                // Base gradient
                let r = Math.floor((x / canvasWidth) * 255);
                let g = Math.floor((y / canvasHeight) * 255);
                let b = Math.floor((distFromCenter / (canvasWidth / 2)) * 255);
                
                // Add circle
                if (distFromCenter < 80) {
                    r = 255;
                    g = 100;
                    b = 100;
                }
                
                // Add rectangle
                if (x > 250 && x < 350 && y > 50 && y < 150) {
                    r = 100;
                    g = 255;
                    b = 100;
                }
                
                // Add noise
                const noise = (Math.random() - 0.5) * 30;
                r = Math.max(0, Math.min(255, r + noise));
                g = Math.max(0, Math.min(255, g + noise));
                b = Math.max(0, Math.min(255, b + noise));
                
                data[idx] = r;
                data[idx + 1] = g;
                data[idx + 2] = b;
                data[idx + 3] = 255;
            }
        }
        
        imageData = imgData;
        originalCtx.putImageData(imgData, 0, 0);
        processedCtx.putImageData(imgData, 0, 0);
    }
    
    // Grayscale conversion
    function toGrayscale(data) {
        const gray = new Uint8ClampedArray(data.length);
        for (let i = 0; i < data.length; i += 4) {
            const avg = Math.floor((data[i] + data[i + 1] + data[i + 2]) / 3);
            gray[i] = avg;
            gray[i + 1] = avg;
            gray[i + 2] = avg;
            gray[i + 3] = 255;
        }
        return gray;
    }
    
    // Apply operations
    function applyOperation() {
        if (!imageData) return;
        
        const operation = operationSelect.value;
        const kernel = parseInt(kernelSizeInput.value);
        const minThresh = parseInt(thresholdMinInput.value);
        const maxThresh = parseInt(thresholdMaxInput.value);
        
        const srcData = imageData.data;
        const resultData = processedCtx.createImageData(canvasWidth, canvasHeight);
        const dst = resultData.data;
        
        switch (operation) {
            case 'adaptive_mean':
                applyAdaptiveThreshold(srcData, dst, kernel, minThresh, maxThresh, 'mean');
                break;
            case 'adaptive_gaussian':
                applyAdaptiveThreshold(srcData, dst, kernel, minThresh, maxThresh, 'gaussian');
                break;
            case 'contours':
                applyFindContours(srcData, dst, minThresh, maxThresh);
                break;
            case 'canny':
                applyCanny(srcData, dst, minThresh, maxThresh);
                break;
            case 'blackhat':
                applyMorphology(srcData, dst, kernel, 'blackhat');
                break;
            case 'erode':
                applyMorphology(srcData, dst, kernel, 'erode');
                break;
            case 'dilate':
                applyMorphology(srcData, dst, kernel, 'dilate');
                break;
            case 'open':
                applyMorphology(srcData, dst, kernel, 'open');
                break;
            case 'close':
                applyMorphology(srcData, dst, kernel, 'close');
                break;
            case 'gradient':
                applyMorphology(srcData, dst, kernel, 'gradient');
                break;
            case 'binary_inv':
                applyBinaryThreshold(srcData, dst, minThresh, maxThresh, true);
                break;
            case 'binary':
                applyBinaryThreshold(srcData, dst, minThresh, maxThresh, false);
                break;
            default:
                processedCtx.putImageData(imageData, 0, 0);
        }
        
        processedCtx.putImageData(resultData, 0, 0);
    }
    
    // Adaptive Threshold
    function applyAdaptiveThreshold(src, dst, blockSize, minVal, maxVal, method) {
        const gray = toGrayscale(src);
        const halfBlock = Math.floor(blockSize / 2);
        
        for (let y = 0; y < canvasHeight; y++) {
            for (let x = 0; x < canvasWidth; x++) {
                let sum = 0;
                let count = 0;
                
                for (let dy = -halfBlock; dy <= halfBlock; dy++) {
                    for (let dx = -halfBlock; dx <= halfBlock; dx++) {
                        const nx = x + dx;
                        const ny = y + dy;
                        if (nx >= 0 && nx < canvasWidth && ny >= 0 && ny < canvasHeight) {
                            const idx = (ny * canvasWidth + nx) * 4;
                            if (method === 'gaussian') {
                                const weight = Math.exp(-(dx*dx + dy*dy) / (2 * halfBlock * halfBlock));
                                sum += gray[idx] * weight;
                                count += weight;
                            } else {
                                sum += gray[idx];
                                count++;
                            }
                        }
                    }
                }
                
                const threshold = sum / count;
                const idx = (y * canvasWidth + x) * 4;
                const pixelVal = gray[idx] > threshold ? maxVal : minVal;
                
                dst[idx] = pixelVal;
                dst[idx + 1] = pixelVal;
                dst[idx + 2] = pixelVal;
                dst[idx + 3] = 255;
            }
        }
    }
    
    // Binary Threshold
    function applyBinaryThreshold(src, dst, minVal, maxVal, inverse) {
        const gray = toGrayscale(src);
        
        for (let i = 0; i < gray.length; i += 4) {
            const val = inverse ? (gray[i] > minVal ? 0 : maxVal) : (gray[i] > minVal ? maxVal : 0);
            dst[i] = val;
            dst[i + 1] = val;
            dst[i + 2] = val;
            dst[i + 3] = 255;
        }
    }
    
    // Find Contours (simplified edge detection)
    function applyFindContours(src, dst, minVal, maxVal) {
        const gray = toGrayscale(src);
        
        for (let y = 1; y < canvasHeight - 1; y++) {
            for (let x = 1; x < canvasWidth - 1; x++) {
                const idx = (y * canvasWidth + x) * 4;
                const center = gray[idx];
                const right = gray[(y * canvasWidth + x + 1) * 4];
                const bottom = gray[((y + 1) * canvasWidth + x) * 4];
                
                const gradient = Math.abs(center - right) + Math.abs(center - bottom);
                const val = gradient > minVal ? maxVal : 0;
                
                dst[idx] = val;
                dst[idx + 1] = val;
                dst[idx + 2] = val;
                dst[idx + 3] = 255;
            }
        }
    }
    
    // Canny Edge Detection (simplified)
    function applyCanny(src, dst, minVal, maxVal) {
        const gray = toGrayscale(src);
        const edges = new Float32Array(gray.length / 4);
        
        // Sobel operator
        for (let y = 1; y < canvasHeight - 1; y++) {
            for (let x = 1; x < canvasWidth - 1; x++) {
                const idx = (y * canvasWidth + x) * 4;
                
                const gx = -gray[((y - 1) * canvasWidth + x - 1) * 4] + gray[((y - 1) * canvasWidth + x + 1) * 4]
                          -2 * gray[(y * canvasWidth + x - 1) * 4] + 2 * gray[(y * canvasWidth + x + 1) * 4]
                          -gray[((y + 1) * canvasWidth + x - 1) * 4] + gray[((y + 1) * canvasWidth + x + 1) * 4];
                
                const gy = -gray[((y - 1) * canvasWidth + x - 1) * 4] - 2 * gray[((y - 1) * canvasWidth + x) * 4] - gray[((y - 1) * canvasWidth + x + 1) * 4]
                          +gray[((y + 1) * canvasWidth + x - 1) * 4] + 2 * gray[((y + 1) * canvasWidth + x) * 4] + gray[((y + 1) * canvasWidth + x + 1) * 4];
                
                edges[y * canvasWidth + x] = Math.sqrt(gx * gx + gy * gy);
            }
        }
        
        // Non-maximum suppression and thresholding
        for (let y = 0; y < canvasHeight; y++) {
            for (let x = 0; x < canvasWidth; x++) {
                const idx = (y * canvasWidth + x) * 4;
                const magnitude = edges[y * canvasWidth + x];
                
                let val = 0;
                if (magnitude > maxVal) {
                    val = 255;
                } else if (magnitude > minVal) {
                    val = 128;
                }
                
                dst[idx] = val;
                dst[idx + 1] = val;
                dst[idx + 2] = val;
                dst[idx + 3] = 255;
            }
        }
    }
    
    // Morphological Operations
    function applyMorphology(src, dst, kernelSize, operation) {
        const gray = toGrayscale(src);
        const halfKernel = Math.floor(kernelSize / 2);
        
        for (let y = 0; y < canvasHeight; y++) {
            for (let x = 0; x < canvasWidth; x++) {
                let values = [];
                
                for (let dy = -halfKernel; dy <= halfKernel; dy++) {
                    for (let dx = -halfKernel; dx <= halfKernel; dx++) {
                        const nx = x + dx;
                        const ny = y + dy;
                        if (nx >= 0 && nx < canvasWidth && ny >= 0 && ny < canvasHeight) {
                            const idx = (ny * canvasWidth + nx) * 4;
                            values.push(gray[idx]);
                        }
                    }
                }
                
                let result;
                switch (operation) {
                    case 'erode':
                        result = Math.min(...values);
                        break;
                    case 'dilate':
                        result = Math.max(...values);
                        break;
                    case 'open':
                        // Erode then dilate (simplified)
                        result = Math.min(...values);
                        break;
                    case 'close':
                        // Dilate then erode (simplified)
                        result = Math.max(...values);
                        break;
                    case 'blackhat':
                        result = 255 - Math.max(...values);
                        break;
                    case 'gradient':
                        result = Math.max(...values) - Math.min(...values);
                        break;
                    default:
                        result = gray[(y * canvasWidth + x) * 4];
                }
                
                const idx = (y * canvasWidth + x) * 4;
                dst[idx] = result;
                dst[idx + 1] = result;
                dst[idx + 2] = result;
                dst[idx + 3] = 255;
            }
        }
    }
    
    // Reset function
    function reset() {
        operationSelect.value = 'none';
        kernelSizeInput.value = 5;
        thresholdMinInput.value = 127;
        thresholdMaxInput.value = 255;
        kernelValue.textContent = '5';
        minValue.textContent = '127';
        maxValue.textContent = '255';
        processedCtx.putImageData(imageData, 0, 0);
    }
    
    // Event listeners
    applyBtn.addEventListener('click', applyOperation);
    resetBtn.addEventListener('click', reset);
    
    operationSelect.addEventListener('change', applyOperation);
    
    kernelSizeInput.addEventListener('input', function() {
        kernelValue.textContent = this.value;
    });
    
    thresholdMinInput.addEventListener('input', function() {
        minValue.textContent = this.value;
    });
    
    thresholdMaxInput.addEventListener('input', function() {
        maxValue.textContent = this.value;
    });
    
    // Initialize
    createSampleImage();
    
    // Smooth scroll for navigation
    document.querySelectorAll('.toc a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
