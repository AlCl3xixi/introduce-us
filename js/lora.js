/* ============================================================
   AI 生图（文生图 / 图生图）- 调用本地 Stable Diffusion WebUI
   ============================================================ */

// ---------- 配置 ----------
const SD_API_BASE = 'http://localhost:7860';
const SD_TXT2IMG = `${SD_API_BASE}/sdapi/v1/txt2img`;
const SD_IMG2IMG = `${SD_API_BASE}/sdapi/v1/img2img`;
const REQUEST_TIMEOUT_MS = 300 * 1000;  // 5 分钟，避免大模型超时
const MAX_IMAGE_SIDE = 512;              // 上传图压缩到最长边 512，减小 payload，也避免 WebUI 再做 resize 出问题
const IMAGE_JPEG_QUALITY = 0.8;

// ---------- 工具函数：文件 -> 压缩后 -> base64（不带前缀） ----------
function fileToCompressedBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                // 等比缩到最大边不超过 MAX_IMAGE_SIDE
                let { width, height } = img;
                const maxSide = Math.max(width, height);
                if (maxSide > MAX_IMAGE_SIDE) {
                    const scale = MAX_IMAGE_SIDE / maxSide;
                    width = Math.round(width * scale);
                    height = Math.round(height * scale);
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                // canvas -> jpeg dataURL -> 切片拿到 base64
                const dataUrl = canvas.toDataURL('image/jpeg', IMAGE_JPEG_QUALITY);
                const comma = dataUrl.indexOf(',');
                resolve(dataUrl.slice(comma + 1));
            };
            img.onerror = () => reject(new Error('图片解码失败'));
            img.src = e.target.result;
        };
        reader.onerror = () => reject(new Error('读取文件失败'));
        reader.readAsDataURL(file);
    });
}

// ---------- 工具函数：读取文件用于预览（不压缩，直接显示小缩略图） ----------
function fileToDataUrl(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject();
        reader.readAsDataURL(file);
    });
}

// ---------- Tab 切换 ----------
function initTabs() {
    const tabs = document.querySelectorAll('#tabBar .tab-btn');
    const panels = document.querySelectorAll('.tab-panel');

    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.tab;
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => {
                if (p.dataset.tab === target) p.classList.add('active');
                else p.classList.remove('active');
            });
            btn.classList.add('active');
        });
    });
}

// ---------- 图片上传处理 ----------
const img2imgState = { init: '' };

function bindUpload(inputId, previewId, stateKey) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    if (!input || !preview) return;

    input.addEventListener('change', async () => {
        const file = input.files && input.files[0];
        if (!file) return;

        try {
            preview.innerHTML = '<span class="upload-hint">正在处理图片...</span>';
            const [dataUrl, b64] = await Promise.all([
                fileToDataUrl(file),
                fileToCompressedBase64(file),
            ]);
            img2imgState[stateKey] = b64;

            preview.innerHTML = '';
            const img = document.createElement('img');
            img.src = dataUrl;
            preview.appendChild(img);

            const meta = document.createElement('span');
            meta.className = 'upload-meta';
            meta.textContent = file.name;
            preview.appendChild(meta);
        } catch (err) {
            preview.innerHTML = `<span class="upload-hint" style="color:#c0392b;">处理失败: ${err.message}</span>`;
        }
    });
}

// ---------- txt2img payload ----------
function buildTxt2ImgPayload() {
    const enableHR = document.getElementById('p-hr').checked;
    const hrSteps = parseInt(document.getElementById('p-hr-steps').value, 10) || 0;

    return {
        prompt: document.getElementById('p-prompt').value.trim(),
        negative_prompt: document.getElementById('p-negative').value.trim(),
        styles: [],
        seed: parseInt(document.getElementById('p-seed').value, 10) || -1,
        subseed: -1,
        subseed_strength: 0,
        seed_resize_from_h: -1,
        seed_resize_from_w: -1,
        sampler_name: document.getElementById('p-sampler').value.trim() || 'Euler a',
        scheduler: document.getElementById('p-scheduler').value.trim() || 'automatic',
        batch_size: parseInt(document.getElementById('p-batch').value, 10) || 1,
        n_iter: parseInt(document.getElementById('p-iter').value, 10) || 1,
        steps: parseInt(document.getElementById('p-steps').value, 10) || 30,
        cfg_scale: parseFloat(document.getElementById('p-cfg').value) || 7,
        width: parseInt(document.getElementById('p-width').value, 10) || 512,
        height: parseInt(document.getElementById('p-height').value, 10) || 512,
        restore_faces: !!document.getElementById('p-restore').checked,
        tiling: false,
        do_not_save_samples: !document.getElementById('p-save').checked,
        do_not_save_grid: !document.getElementById('p-save').checked,
        eta: 0,
        denoising_strength: parseFloat(document.getElementById('p-hr-denoise').value) || 0.4,
        override_settings: {},
        override_settings_restore_afterwards: true,
        refiner_checkpoint: '',
        refiner_switch_at: 0,
        disable_extra_networks: false,
        firstpass_image: '',
        comments: {},
        enable_hr: enableHR,
        firstphase_width: 0,
        firstphase_height: 0,
        hr_scale: enableHR ? (parseFloat(document.getElementById('p-hr-scale').value) || 2) : 2,
        hr_upscaler: enableHR ? (document.getElementById('p-hr-upscaler').value || 'ESRGAN_4x') : '',
        hr_second_pass_steps: enableHR ? hrSteps : 0,
        hr_resize_x: 0,
        hr_resize_y: 0,
        hr_checkpoint_name: '',
        hr_sampler_name: '',
        hr_scheduler: '',
        hr_prompt: '',
        hr_negative_prompt: '',
        force_task_id: '',
        sampler_index: document.getElementById('p-sampler').value.trim() || 'Euler a',
        script_name: '',
        script_args: [],
        send_images: true,
        save_images: !!document.getElementById('p-save').checked,
        alwayson_scripts: {},
        infotext: '',
    };
}

// ---------- img2img payload ----------
// 最小字段集：不做局部重绘蒙版，只用整图风格变换
function buildImg2ImgPayload() {
    const images = img2imgState.init ? [img2imgState.init] : [];

    return {
        prompt: document.getElementById('i-prompt').value.trim(),
        negative_prompt: document.getElementById('i-negative').value.trim(),
        seed: parseInt(document.getElementById('i-seed').value, 10) || -1,
        sampler_name: document.getElementById('i-sampler').value.trim() || 'Euler a',
        scheduler: document.getElementById('i-scheduler').value.trim() || 'automatic',
        batch_size: parseInt(document.getElementById('i-batch').value, 10) || 1,
        n_iter: parseInt(document.getElementById('i-iter').value, 10) || 1,
        steps: parseInt(document.getElementById('i-steps').value, 10) || 30,
        cfg_scale: parseFloat(document.getElementById('i-cfg').value) || 7,
        width: parseInt(document.getElementById('i-width').value, 10) || 768,
        height: parseInt(document.getElementById('i-height').value, 10) || 768,
        denoising_strength: parseFloat(document.getElementById('i-denoise').value) || 0.75,
        init_images: images,
        resize_mode: parseInt(document.getElementById('i-resize').value, 10) || 2,
        send_images: true,
        save_images: !!document.getElementById('i-save').checked,
    };
}

// ---------- 统一请求 ----------
async function callSdApi(url, payload, statusEl, resultEl, btn) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    setStatus(statusEl, '正在生成图片，请稍候...', 'running');
    resultEl.innerHTML = '';
    btn.disabled = true;
    btn.classList.add('loading');

    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            signal: controller.signal,
        });

        if (!res.ok) {
            // 500 / 422 等错误——WebUI 会返回 JSON {detail: "..."}，解析出来展示
            let detail = '';
            try {
                const text = await res.text();
                try {
                    const j = JSON.parse(text);
                    detail = j.detail || j.message || j.error || j.msg || text;
                    if (Array.isArray(detail)) {
                        detail = detail.map(d => (d && (d.msg || d.message || d.loc || JSON.stringify(d)))).join('; ');
                    }
                } catch (_) {
                    detail = text;
                }
            } catch (_) {}
            throw new Error(`HTTP ${res.status} ${res.statusText}\n${detail}`);
        }

        const data = await res.json();
        const images = data.images || [];
        if (images.length === 0) throw new Error('WebUI 未返回任何图片');

        renderResult(images, resultEl);

        // 尝试展示 seed
        if (data.info) {
            try {
                const info = typeof data.info === 'string' ? JSON.parse(data.info) : data.info;
                const seedInfo = document.createElement('div');
                seedInfo.className = 'result-meta';
                seedInfo.textContent = `本次 seed: ${info.seed ?? '(未知)'}  共 ${images.length} 张`;
                resultEl.prepend(seedInfo);
            } catch (_) {}
        }
        setStatus(statusEl, `✅ 生成成功，共 ${images.length} 张`, 'success');
    } catch (err) {
        console.error(err);
        let msg = err.message || String(err);

        if (err.name === 'AbortError') {
            msg = `请求超时（${Math.round(REQUEST_TIMEOUT_MS / 1000)} 秒），可降低 batch / 尺寸后重试。`;
        } else if (/Failed to fetch|NetworkError|net::|TypeError.*fetch/i.test(msg)) {
            msg =
                '❌ 请求被浏览器拒绝（但文生图已能通，CORS 与 API 应该是正常的）。\n' +
                '请按下面步骤排查 / 操作：\n' +
                '① 按 F12 → Network（网络）面板，勾选「Preserve log」（保留日志）\n' +
                '② 重新点一次图生图的生成按钮\n' +
                '③ 看红色那个 /sdapi/v1/img2img 请求，把「Status」与「Headers」里的错误发我\n' +
                '④ 若是 “(blocked:mixed-content)” / “(blocked:origin)” 开头 → 改一下预览页 URL\n' +
                '⑤ 若是 404 / 500 / 红色其它状态码 → 看 Response 里 JSON 里的 detail 字段\n' +
                '\n先执行上面 ①②③，再告诉我看到的错误信息，我帮你直接诊断。';
        }
        setStatus(statusEl, msg, 'error');
    } finally {
        clearTimeout(timer);
        btn.disabled = false;
        btn.classList.remove('loading');
    }
}

function renderResult(images, resultEl) {
    const grid = document.createElement('div');
    grid.className = 'result-grid';

    images.forEach((b64, i) => {
        const card = document.createElement('div');
        card.className = 'result-card';

        const img = document.createElement('img');
        img.src = `data:image/png;base64,${b64}`;
        img.alt = `result-${i + 1}`;

        const actions = document.createElement('div');
        actions.className = 'result-actions';

        const dl = document.createElement('a');
        dl.href = img.src;
        dl.download = `sd_${Date.now()}_${i + 1}.png`;
        dl.className = 'btn-download';
        dl.textContent = '下载';

        actions.appendChild(dl);
        card.appendChild(img);
        card.appendChild(actions);
        grid.appendChild(card);
    });

    resultEl.appendChild(grid);
}

function setStatus(el, text, type) {
    if (!el) return;
    el.textContent = text;
    el.className = 'status-text' + (type ? ' status-' + type : '');
    el.style.whiteSpace = 'pre-line';
}

// ---------- 初始化 ----------
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    bindUpload('i-init', 'i-init-preview', 'init');

    // txt2img
    const txtBtn = document.getElementById('p-generate');
    if (txtBtn) {
        txtBtn.addEventListener('click', () => {
            const prompt = document.getElementById('p-prompt').value.trim();
            const statusEl = document.getElementById('p-status');
            const resultEl = document.getElementById('gen-result');
            if (!prompt) {
                setStatus(statusEl, '请先填写正向提示词 (Prompt)', 'error');
                return;
            }
            callSdApi(SD_TXT2IMG, buildTxt2ImgPayload(), statusEl, resultEl, txtBtn);
        });
    }

    // img2img
    const imgBtn = document.getElementById('i-generate');
    if (imgBtn) {
        imgBtn.addEventListener('click', () => {
            const prompt = document.getElementById('i-prompt').value.trim();
            const statusEl = document.getElementById('i-status');
            const resultEl = document.getElementById('gen-result');
            if (!prompt) {
                setStatus(statusEl, '请先填写正向提示词 (Prompt)', 'error');
                return;
            }
            if (!img2imgState.init) {
                setStatus(statusEl, '请先上传一张底图', 'error');
                return;
            }
            callSdApi(SD_IMG2IMG, buildImg2ImgPayload(), statusEl, resultEl, imgBtn);
        });
    }

    // HR 勾选项的联动展开
    const hrBox = document.getElementById('p-hr');
    if (hrBox) {
        const hrPanel = document.getElementById('p-hr-panel');
        hrBox.addEventListener('change', () => {
            hrPanel.style.display = hrBox.checked ? 'grid' : 'none';
        });
    }
});
