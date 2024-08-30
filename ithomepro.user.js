// ==UserScript==
// @name         IThome Pro - IT之家高级优化版 2024
// @version      3.2
// @description  优化ithome网页端浏览效果
// @match        https://www.ithome.com/*
// @run-at       document-start
// @namespace    https://greasyfork.org/users/1354671
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
    }, 5000);

    // Redirect from homepage to blog page
    if (window.location.href === 'https://www.ithome.com/') {
        const style = document.createElement('style');
        style.innerHTML = `body { opacity: 0; }`;
        document.head.appendChild(style);
        window.location.replace('https://www.ithome.com/blog/');
        return;
    }

    // Initial CSS to hide the entire page before it fully loads
    const style = document.createElement('style');
    style.innerHTML = `
        body { opacity: 0; } /* 立即隐藏页面，无过渡效果 */
    `;
    document.head.appendChild(style);

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
            '[id^="ad-id-"]'
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

        if (image.closest('a.img')) {
            const anchor = image.closest('a.img');
            if (!anchor.classList.contains('processed')) { // 检查是否已经处理过
                anchor.style.border = '3px solid #CCC';
                anchor.style.borderRadius = '12px';
                anchor.style.display = 'inline-block';
                anchor.style.overflow = 'hidden';
                anchor.classList.add('processed'); // 标记为已处理
            }
        } else if (image.closest('.ithome_super_player')) {
            const videoPlayer = image.closest('.ithome_super_player');
            if (!videoPlayer.parentNode.classList.contains('processed')) { // 检查是否已经处理过
                const wrapper = document.createElement('div');
                wrapper.style.border = '3px solid #CCC';
                wrapper.style.borderRadius = '12px';
                wrapper.style.overflow = 'hidden';
                wrapper.style.maxWidth = '100%';  // 设置最大宽度为100%
                wrapper.style.display = 'block';
                wrapper.style.margin = '0 auto';
                wrapper.classList.add('processed'); // 标记为已处理
                videoPlayer.parentNode.insertBefore(wrapper, videoPlayer);
                wrapper.appendChild(videoPlayer);

                // 设置预览图根据父元素高度调整
                const img = videoPlayer.querySelector('img');
                if (img) {
                    const imgWidth = img.getAttribute('w'); // 获取图片的宽度属性
                    const imgHeight = img.getAttribute('h'); // 获取图片的高度属性
                    const parentHeight = wrapper.offsetHeight;

                    if (imgWidth > wrapper.offsetWidth) {
                        const aspectRatio = imgWidth / imgHeight;
                        img.style.height = `${parentHeight}px`; // 高度匹配父元素高度
                        img.style.width = `${parentHeight * aspectRatio}px`; // 根据高度和宽高比自动调整宽度
                        img.style.objectFit = 'cover'; // 确保图片覆盖整个区域
                    } else {
                        img.style.width = `${imgWidth}px`; // 使用图片的默认宽度
                        img.style.height = `${imgHeight}px`; // 使用图片的默认高度
                    }
                }
            }
        } else {
            // 头像修正
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
            if (!iframe.classList.contains('processed')) { // 检查是否已经处理过
                iframe.style.borderRadius = '12px';
                iframe.style.border = '3px solid #CCC';
                iframe.style.display = 'block';
                iframe.style.margin = '0 auto';
                iframe.style.overflow = 'hidden';
                iframe.classList.add('processed'); // 标记为已处理
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
    function decodeAndDisplayImage(node) {
        const span = node.querySelector('span.img-placeholder');
        if (span) {
            const dataS = span.getAttribute('data-s');
            if (dataS) {
                const decodedUrl = atob(dataS);
                const img = document.createElement('img');
                img.src = decodedUrl;
                img.classList.add('comment-image'); // 给评论区的图片添加特征
                img.style.maxWidth = '200px'; // 设置初始最大宽度为200px
                img.style.display = 'block'; // 让图片作为块级元素
                img.style.marginLeft = '0'; // 确保图片居左对齐
                img.style.border = '1px solid rgb(204, 204, 204)'; // 设置边框颜色和宽度
                img.style.borderRadius = '12px'; // 设置图片圆角
                img.style.cursor = 'pointer'; // 设置鼠标悬停时为手型光标，表示图片可点击

                let isZoomed = false; // 标志位，表示图片是否放大

                img.addEventListener('click', function() {
                    if (!isZoomed) {
                        // 放大图片
                        img.style.maxWidth = '100%'; // 将图片的最大宽度设置为父元素宽度
                        img.style.height = 'auto'; // 自动调整高度以保持宽高比
                        img.style.cursor = 'zoom-out'; // 鼠标悬停时变为缩小光标
                        isZoomed = true;
                    } else {
                        // 恢复图片到初始状态
                        img.style.maxWidth = '200px'; // 恢复到初始宽度200px
                        img.style.height = 'auto'; // 自动调整高度以保持宽高比
                        img.style.cursor = 'pointer'; // 鼠标悬停时变为放大光标
                        isZoomed = false;
                    }
                });

                span.innerHTML = ''; // 清空span内容
                span.appendChild(img); // 添加img元素
            }
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
                    handleNewNodes(mutation.addedNodes); // Handle new comment images
                }
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    // Initial processing for existing comment images
    document.querySelectorAll('.post-img-list.c-1').forEach((node) => {
        decodeAndDisplayImage(node);
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
        document.body.style.opacity = '1'; // 页面加载完成后显示内容

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