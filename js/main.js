/* ============================================================
   主要交互脚本
   ============================================================ */

// ------------------------------------------------------------
// 1. 移动端导航切换
// ------------------------------------------------------------
(function initNav() {
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('navMenu');
    if (!toggle || !menu) return;

    toggle.addEventListener('click', () => {
        menu.classList.toggle('active');
    });

    // 点击菜单项后自动收起（仅移动端）
    menu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 640) {
                menu.classList.remove('active');
            }
        });
    });
})();

// ------------------------------------------------------------
// 2. 团队成员配置
//    在 images/team/ 目录下放图片，然后在此处填写真实信息；
//    目前使用占位卡片（HTML 中已写好 4 张占位）。
// ------------------------------------------------------------
const teamMembers = [
    // { name: '张三', role: '队长', bio: '负责项目统筹', avatar: 'images/team/1.jpg' },
    // { name: '李四', role: '宣传员', bio: '负责图文记录', avatar: 'images/team/2.jpg' },
    // ...
];

function renderTeam() {
    const grid = document.getElementById('teamGrid');
    if (!grid || teamMembers.length === 0) return;
    grid.innerHTML = '';
    teamMembers.forEach((m) => {
        const card = document.createElement('div');
        card.className = 'team-card';
        card.innerHTML = `
            <div class="team-avatar"><img src="${m.avatar}" alt="${m.name}" loading="lazy"></div>
            <h3 class="team-name">${m.name}</h3>
            <p class="team-role">${m.role}</p>
            <p class="team-bio">${m.bio}</p>
        `;
        grid.appendChild(card);
    });
}

// ------------------------------------------------------------
// 3. 图片画廊
//    方案 A（推荐）：在 galleryImages 数组里填入 50 张图片路径。
//    方案 B：按命名约定自动生成（下方已提供示例，文件名从 1.jpg 到 50.jpg）。
// ------------------------------------------------------------
const galleryImages = [
    // 'images/gallery/1.jpg',
    // 'images/gallery/2.jpg',
    // 'images/gallery/3.jpg',
    // ... 约 50 张
];

// 如果 galleryImages 为空，则自动生成 50 个占位项（便于调试样式）
function buildGalleryList() {
    if (galleryImages.length > 0) return galleryImages;
    const list = [];
    for (let i = 1; i <= 50; i++) {
        list.push(`images/gallery/${i}.jpg`);
    }
    return list;
}

function renderGallery() {
    const grid = document.getElementById('galleryGrid');
    if (!grid) return;

    const list = buildGalleryList();
    grid.innerHTML = '';

    list.forEach((src, idx) => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        const img = document.createElement('img');
        img.src = src;
        img.loading = 'lazy';
        img.alt = '活动图片 ' + (idx + 1);
        img.title = '活动图片 ' + (idx + 1);
        img.addEventListener('load', () => img.classList.add('loaded'));
        img.addEventListener('click', () => openLightbox(src, img.alt));
        item.appendChild(img);
        grid.appendChild(item);
    });
}

// ------------------------------------------------------------
// 4. 图片 Lightbox 放大查看
// ------------------------------------------------------------
let lightbox, lightboxImg, lightboxClose;

function openLightbox(src, altText) {
    if (!lightbox) {
        lightbox = document.getElementById('lightbox');
        lightboxImg = document.getElementById('lightboxImg');
        lightboxClose = document.getElementById('lightboxClose');
        lightboxClose.addEventListener('click', closeLightbox);
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });
    }
    lightboxImg.src = src;
    lightboxImg.alt = altText || '活动图片';
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
});

// ------------------------------------------------------------
// 5. 初始化
// ------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    renderTeam();
    renderGallery();
    preloadGameImages();
});

// ------------------------------------------------------------
// 6. 游戏图片预加载
//    在用户浏览主页面时后台加载游戏资源，提升进入游戏的速度
//    分优先级加载：高优先级立即加载，中优先级延迟加载，低优先级空闲时加载
// ------------------------------------------------------------
function preloadGameImages() {
    const highPriority = [
        'game/images/bg.jpg',
        'game/images/covers/mudan.jpg',
        'game/images/covers/fenghuang.jpg',
        'game/images/covers/long.jpg',
        'game/images/puzzle/mudan-preview.jpg',
        'game/images/puzzle/fenghuang-preview.jpg',
        'game/images/puzzle/long-preview.jpg',
    ];
    
    const mediumPriority = [
        'game/images/puzzle/mudan-full.jpg',
        'game/images/puzzle/mudan-1.png',
        'game/images/puzzle/mudan-2.png',
        'game/images/puzzle/mudan-3.png',
        'game/images/puzzle/mudan-1-s.png',
        'game/images/puzzle/mudan-2-s.png',
        'game/images/puzzle/mudan-3-s.png',
        'game/images/puzzle/fenghuang-1.png',
        'game/images/puzzle/fenghuang-2.png',
        'game/images/puzzle/fenghuang-3.png',
        'game/images/puzzle/fenghuang-4.png',
        'game/images/puzzle/fenghuang-1-s.png',
        'game/images/puzzle/fenghuang-2-s.png',
        'game/images/puzzle/fenghuang-3-s.png',
        'game/images/puzzle/fenghuang-4-s.png',
        'game/images/puzzle/long-1.png',
        'game/images/puzzle/long-2.png',
        'game/images/puzzle/long-3.png',
        'game/images/puzzle/long-4.png',
        'game/images/puzzle/long-5.png',
        'game/images/puzzle/long-1-s.png',
        'game/images/puzzle/long-2-s.png',
        'game/images/puzzle/long-3-s.png',
        'game/images/puzzle/long-4-s.png',
        'game/images/puzzle/long-5-s.png',
    ];
    
    const lowPriority = [
        'game/images/puzzle/mudan-delineate.webp',
        'game/images/puzzle/fenghuang-delineate.webp',
        'game/images/puzzle/long-delineate.webp',
        'game/images/ceramic/mudan-1-whole.webp',
        'game/images/ceramic/mudan-1-broken.webp',
        'game/images/ceramic/mudan-2-whole.webp',
        'game/images/ceramic/mudan-2-broken.webp',
        'game/images/ceramic/mudan-3-whole.webp',
        'game/images/ceramic/mudan-3-broken.webp',
        'game/images/ceramic/fenghuang-1-whole.webp',
        'game/images/ceramic/fenghuang-1-broken.webp',
        'game/images/ceramic/fenghuang-2-whole.webp',
        'game/images/ceramic/fenghuang-2-broken.webp',
        'game/images/ceramic/fenghuang-3-whole.webp',
        'game/images/ceramic/fenghuang-3-broken.webp',
        'game/images/ceramic/fenghuang-4-whole.webp',
        'game/images/ceramic/fenghuang-4-broken.webp',
        'game/images/ceramic/long-1-whole.webp',
        'game/images/ceramic/long-1-broken.webp',
        'game/images/ceramic/long-2-whole.webp',
        'game/images/ceramic/long-2-broken.webp',
        'game/images/ceramic/long-3-whole.webp',
        'game/images/ceramic/long-3-broken.webp',
        'game/images/ceramic/long-4-whole.webp',
        'game/images/ceramic/long-4-broken.webp',
        'game/images/ceramic/long-5-whole.webp',
        'game/images/ceramic/long-5-broken.webp',
    ];
    
    function loadImages(urls) {
        urls.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }
    
    loadImages(highPriority);
    
    setTimeout(() => {
        loadImages(mediumPriority);
    }, 500);
    
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            loadImages(lowPriority);
        }, { timeout: 3000 });
    } else {
        setTimeout(() => {
            loadImages(lowPriority);
        }, 1500);
    }
}
