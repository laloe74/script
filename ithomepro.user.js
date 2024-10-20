// ==UserScript==
// @name         IThome Pro - IT之家高级优化版 2024
// @version      3.9
// @description  优化ithome网页端浏览效果
// @match        *://*.ithome.com/*
// @run-at       document-start
// @namespace    https://greasyfork.org/users/1354671
// @downloadURL  https://update.greasyfork.org/scripts/504286/IThome%20Pro%20-%20IT%E4%B9%8B%E5%AE%B6%E9%AB%98%E7%BA%A7%E4%BC%98%E5%8C%96%E7%89%88%202024.user.js
// @updateURL    https://update.greasyfork.org/scripts/504286/IThome%20Pro%20-%20IT%E4%B9%8B%E5%AE%B6%E9%AB%98%E7%BA%A7%E4%BC%98%E5%8C%96%E7%89%88%202024.meta.js
// ==/UserScript==

(function() {
    'use strict';

    // Function to keep the page active by simulating clicks
    function keepPageActive() {
        const event = new MouseEvent('click', {
            view: window,
            bubbles: true,
            cancelable: true,
            clientX: 0, // 点击页面左上角，通常是空白区域
            clientY: 0
        });
        document.dispatchEvent(event);
    }

    // Set an interval to keep the page active every 0.2 seconds
    const intervalId = setInterval(keepPageActive, 200);

    // Stop the interval after 5 seconds
    setTimeout(() => {
        clearInterval(intervalId);
    }, 1000);

    // 定义样式用于立即隐藏页面内容
    const hideStyle = document.createElement('style');
    hideStyle.innerHTML = `body { opacity: 0; }`;
    document.head.appendChild(hideStyle);

    // 针对 https://www.ithome.com 页面执行逻辑
    if (window.location.href === 'https://www.ithome.com' || window.location.href === 'https://www.ithome.com/') {
        // 立即隐藏 主页 页面内容
        document.head.appendChild(hideStyle);
        // 跳转到 blog 页面
        window.location.replace('https://www.ithome.com/blog/');
        return;
    }

    // 针对 https://www.ithome.com/blog/ 页面执行逻辑
    if (window.location.href.startsWith('https://www.ithome.com/blog/')) {
        // 立即隐藏 blog 页面内容
        document.head.appendChild(hideStyle);
    }

    // Function to hide elements based on AdGuard rules
    function hideElements() {
        const selectors = [
            '#nav', '#top', '#tt', '#list > div.fr.fx:last-child', '#side_func',
            '#dt > div.fl.content:first-child > div.cv:first-child', '#dt > div.fr.fx:last-child',
            '#dt > div.fl.content:first-child > div.newsgrade:nth-child(6)',
            '#dt > div.fl.content:first-child > div.shareto:nth-child(7)',
            '#dt > div.fl.content:first-child > iframe.dajia:nth-child(10)',
            '#dt > div.fl.content:first-child > div.newsgrade:nth-child(8)',
            '#dt > div.fl.content:first-child > div.newserror:nth-child(7)',
            '#dt > div.fl.content:first-child > div.newsreward:nth-child(6)',
            '#dt > div.fl.content:first-child > div.shareto:nth-child(9)',
            '#rm-login-modal > div.modal.has-title.loaded',
            '#dt > div.fl.content:first-child > div.related_post:nth-child(8)',
            '#dt > div.fl.content:first-child > div.newserror:nth-child(5)',
            '#paragraph > p.ad-tips:last-child', '#postcomment3', '#fls', '#fi', '#lns',
            '#paragraph > div.tougao-user:nth-child(2)', '#login-guide-box', '.dajia',
            '#paragraph > div.tagging1:last-child',
            '#paragraph > p.ad-tips',
            '[id^="ad-id-"]',
            'div.-hongbao-container.bb:nth-child(6)',
        ];

        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                element.style.display = 'none';
            });
        });
    }

    // Function to process and set rounded images
    function processImage(image) {
        if (image.classList.contains('titleLogo')) return;
        if (image.classList.contains('lazy') && image.classList.contains('emoji')) return;
        if (image.classList.contains('ruanmei-emoji') && image.classList.contains('emoji')) return;
        if (image.id === 'image-viewer' || image.classList.contains('zoomed')) return;
        if (image.classList.contains('comment-image')) return; // 排除带有评论区特征的图片
       
        // 图片
        if (image.closest('a.img')) {
            const anchor = image.closest('a.img');
            if (!anchor.classList.contains('processed')) {
                anchor.style.border = '3px solid #CCC';
                anchor.style.borderRadius = '12px';
                anchor.style.display = 'inline-block';
                anchor.style.overflow = 'hidden';
                anchor.classList.add('processed');
            }
        // 视频
        } else if (image.closest('.ithome_super_player')) {
            const videoPlayer = image.closest('.ithome_super_player');
            if (!videoPlayer.parentNode.classList.contains('processed')) {
                const wrapper = document.createElement('div');
                wrapper.style.border = '3px solid #CCC';
                wrapper.style.borderRadius = '12px';
                wrapper.style.overflow = 'hidden';
                wrapper.style.maxWidth = '100%';
                wrapper.style.display = 'block';
                wrapper.style.margin = '0 auto';
                wrapper.classList.add('processed');
                videoPlayer.parentNode.insertBefore(wrapper, videoPlayer);
                wrapper.appendChild(videoPlayer);

                // 设置预览图根据父元素高度调整
                const img = videoPlayer.querySelector('img');
                if (img) {
                    const imgWidth = img.getAttribute('w');
                    const imgHeight = img.getAttribute('h');
                    const parentHeight = wrapper.offsetHeight;

                    if (imgWidth > wrapper.offsetWidth) {
                        const aspectRatio = imgWidth / imgHeight;
                        img.style.height = `${parentHeight}px`;
                        img.style.width = `${parentHeight * aspectRatio}px`;
                        img.style.objectFit = 'cover';
                    } else {
                        img.style.width = `${imgWidth}px`;
                        img.style.height = `${imgHeight}px`;
                    }
                }
            }
        // 头像修正
        } else {
            if (image.width >= 30) {
                image.style.borderRadius = '12px';
                image.style.border = '3px solid #CCC';
            }
            if (image.width >= 30 && image.height > 150) {
                image.style.borderRadius = '12px';
                image.style.border = '3px solid #CCC';
                image.style.maxWidth = '400px';
                image.style.height = 'auto';
                image.style.objectFit = 'cover';
                image.style.overflow = 'hidden';
            }
        }
    }

    // Function to set rounded images on all img elements
    function setRoundedImages() {
        document.querySelectorAll('img').forEach(image => processImage(image));
    }

    // Function to wrap images in <p> tags
    function wrapImagesInP() {
        if (window.location.href.startsWith('https://www.ithome.com/blog/')) return;
        document.querySelectorAll('img').forEach(image => {
            if (image.closest('.ithome_super_player')) return;
            if (image.classList.contains('ruanmei-emoji') && image.classList.contains('emoji')) return;
            if (image.classList.contains('ithome_super_player')) return;
            if (image.parentNode.tagName.toLowerCase() === 'p' && image.parentNode.children.length === 1) return;
            if (image.width < 25 || image.height < 20) return; // 排除编辑标识
            const p = document.createElement('p');
            p.style.textAlign = 'center';
            p.style.margin = '0';
            p.setAttribute('data-vmark', 'f5e8');
            image.parentNode.insertBefore(p, image);
            p.appendChild(image);
        });
    }

    // Function to process specific iframes
    function processIframes() {
        const iframes = document.querySelectorAll('.content .post_content iframe.ithome_video, .content .post_content iframe[src*="player.bilibili.com"]');

        iframes.forEach(iframe => {
            if (!iframe.classList.contains('processed')) {
                iframe.style.borderRadius = '12px';
                iframe.style.border = '3px solid #CCC';
                iframe.style.display = 'block';
                iframe.style.margin = '0 auto';
                iframe.style.overflow = 'hidden';
                iframe.classList.add('processed');
            }
        });
    }

    // Function to set rounded corners for comments
    function setRounded() {
        const roundeds = document.querySelectorAll(
            '.comm_list ul.list li.entry ul.reply, .content .post_content blockquote, ' +
            '.add_comm input#btnComment, .card, span.card'
        );
        roundeds.forEach(rounded => rounded.style.borderRadius = '12px');

        document.querySelectorAll('.add_comm').forEach(addCommElement => {
            addCommElement.style.borderRadius = '0px 0px 12px 12px';
        });

        document.querySelectorAll('.card, span.card').forEach(card => {
            card.style.borderRadius = '12px';
            card.style.transform = 'scale(0.8)';
        });
    }

    // Function to remove specific ads
    function removeAds() {
        document.querySelectorAll('div.bb.clearfix > div.fl > ul.bl > li').forEach(element => {
            if (element.querySelector('div.c > div.m:empty')) element.remove();
        });
    }

    // Automatically click the "Load More" button
    function autoClickLoadMore() {
        const loadMoreButton = document.querySelector('a.more');

        if (loadMoreButton) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        loadMoreButton.click();
                    }
                });
            });

            observer.observe(loadMoreButton);

            // 监听DOM变化，重新观察按钮
            const mutationObserver = new MutationObserver(() => {
                const newLoadMoreButton = document.querySelector('a.more');
                if (newLoadMoreButton && !observer.observe(newLoadMoreButton)) {
                    observer.observe(newLoadMoreButton);
                }
            });

            mutationObserver.observe(document.body, { childList: true, subtree: true });
        }
    }

    // Function to handle new nodes for comment images
    function handleNewNodes(nodes) {
        nodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                if (node.matches('.post-img-list.c-1')) {
                    decodeAndDisplayImage(node);
                }
                // 递归处理子节点
                node.querySelectorAll('.post-img-list.c-1').forEach((childNode) => {
                    decodeAndDisplayImage(childNode);
                });
            }
        });
    }

// Function to decode and display images in comments
function decodeAndDisplayImages(node) {
    try {
        // 获取当前容器中所有的 img-placeholder
        const spanList = node.querySelectorAll('span.img-placeholder');
        spanList.forEach(span => {
            const dataS = span.getAttribute('data-s');
            if (dataS) {
                let decodedUrl;
                try {
                    decodedUrl = atob(dataS); // 解码 Base64 字符串
                } catch (error) {
                    console.error("图片 URL 解码失败：", error, dataS);
                    return; // 解码失败时退出
                }

                const img = document.createElement('img');
                img.src = decodedUrl;
                img.classList.add('comment-image');
                img.style.maxWidth = '200px';
                img.style.display = 'block';
                img.style.marginLeft = '0';
                img.style.border = '1px solid rgb(204, 204, 204)';
                img.style.borderRadius = '12px';
                img.style.cursor = 'pointer';

                let isZoomed = false;
                img.addEventListener('click', function () {
                    if (!isZoomed) {
                        img.style.maxWidth = '100%';
                        img.style.height = 'auto';
                        img.style.cursor = 'zoom-out';
                        isZoomed = true;
                    } else {
                        img.style.maxWidth = '200px';
                        img.style.height = 'auto';
                        img.style.cursor = 'pointer';
                        isZoomed = false;
                    }
                });

                span.innerHTML = ''; // 清空 span 内容
                span.appendChild(img); // 添加 img 元素
            }
        });
    } catch (e) {
        console.error("处理图片时出错：", e, node);
    }
}

    // Observe DOM changes and apply styles/changes dynamically
    function observeDOM() {
        const observer = new MutationObserver(mutationsList => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    setRoundedImages();
                    wrapImagesInP();
                    setRounded();
                    removeAds();
                    hideElements();
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // 检查是否是图片列表并进行处理
                            if (node.matches('.post-img-list')) {
                                decodeAndDisplayImages(node);
                            }
                            // 检查新加入的节点内部是否包含图片列表
                            node.querySelectorAll('.post-img-list').forEach((childNode) => {
                                decodeAndDisplayImages(childNode);
                            });
                        }
                    });
                    wrapImagesInP();
                }
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    // Initial processing for existing comment images
    document.querySelectorAll('.post-img-list.c-1').forEach((node) => {
        decodeAndDisplayImage(node);
    });

    document.querySelectorAll('.post-img-list').forEach((node) => {
        decodeAndDisplayImages(node);
    });

    // Event listeners
    window.addEventListener('scroll', autoClickLoadMore);
    window.addEventListener('load', function() {
        hideElements();
        removeAds();
        wrapImagesInP();
        setRoundedImages();
        setRounded();
        processIframes();
        observeDOM();
        removeAds();
        wrapImagesInP();
        document.body.style.opacity = '1';

        // 处理图片懒加载
        document.querySelectorAll('img').forEach(img => {
            if (img.hasAttribute('loading')) {
                img.removeAttribute('loading');
            }
            if (img.classList.contains('lazy')) {
                img.classList.remove('lazy');
            }
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
            if (img.dataset.original) {
                img.src = img.dataset.original;
            }
            img.loading = 'eager';
        });
    });

})();