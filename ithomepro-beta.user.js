// ==UserScript==
// @name         IThome Pro - Beta
// @version      3.8.1
// @description  优化ithome网页端浏览效果
// @match        *://*.ithome.com/*
// @run-at       document-start
// @namespace    https://greasyfork.org/users/1354671
// @downloadURL  https://update.greasyfork.org/scripts/504286/IThome%20Pro%20-%20IT%E4%B9%8B%E5%AE%B6%E9%AB%98%E7%BA%A7%E4%BC%98%E5%8C%96%E7%89%88%202024.user.js
// @updateURL    https://update.greasyfork.org/scripts/504286/IThome%20Pro%20-%20IT%E4%B9%8B%E5%AE%B6%E9%AB%98%E7%BA%A7%E4%BC%98%E5%8C%96%E7%89%88%202024.meta.js
// ==/UserScript==

(function() {
    'use strict';

    // 定义样式-hideStyle：不透明度 0
    const hideStyle = document.createElement('style');
    hideStyle.innerHTML = `body { opacity: 0; }`;
    document.head.appendChild(hideStyle);

    // 跳转到 blog 页面，加载完成前隐藏原始页面
    if (window.location.href === 'https://www.ithome.com' || window.location.href === 'https://www.ithome.com/') {
        document.head.appendChild(hideStyle);
        window.location.replace('https://www.ithome.com/blog/');
        return;
    }

    // blog 页面加载完成前隐藏原始页面
    if (window.location.href.startsWith('https://www.ithome.com/blog/')) {
        document.head.appendChild(hideStyle);
    }

    // 函数：保持页面激活，这样可以去除弹出的登录框
    function keepPageActive() {
        const event = new Event('mousemove', { bubbles: true, cancelable: true });
        
        // 设置定时器，每0.1秒触发一次事件
        const intervalId = setInterval(() => {
            document.dispatchEvent(event);
        }, 100); // 0.1秒（100毫秒）
    
        // 5秒后停止定时器
        setTimeout(() => {
            clearInterval(intervalId);
            console.log('Stopped keeping page active.');
        }, 5000); // 5秒（5000毫秒）
    }

    // [调用] 保持页面激活
    keepPageActive();


    // 函数：净化页面 利用 AdGuard 规则
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

    // 函数：图片处理 - 圆角、边框
    function processImage(image) {
        // 这部分匹配到的图片不处理
        if (image.classList.contains('titleLogo')) return;
        if (image.classList.contains('lazy') && image.classList.contains('emoji')) return;
        if (image.classList.contains('ruanmei-emoji') && image.classList.contains('emoji')) return;
        if (image.id === 'image-viewer' || image.classList.contains('zoomed')) return;
        if (image.classList.contains('comment-image')) return;
       
        // 首页图片
        if (image.closest('a.img')) {
            const anchor = image.closest('a.img');
            if (!anchor.classList.contains('processed')) {
                anchor.style.border = '3px solid #CCC';
                anchor.style.borderRadius = '12px';
                anchor.style.display = 'inline-block';
                anchor.style.overflow = 'hidden';
                anchor.classList.add('processed');
            }
        // 视频预览图
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

                // 视频预览图根据父元素高度调整
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
        } else {
            // 常规图片
            if (image.width >= 30) {
                image.style.borderRadius = '12px';
                image.style.border = '3px solid #CCC';
            }
            // 限制图片最大宽度 - 解决正文里长图过多的问题
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

    // [调用] 图片处理
    function setRoundedImages() {
        document.querySelectorAll('img').forEach(image => processImage(image));
    }

    // 函数：多图连续排列时插入间隔
    function wrapImagesInP() {
        if (window.location.href.startsWith('https://www.ithome.com/blog/')) return;
        document.querySelectorAll('img').forEach(image => {
            // 这部分匹配到的图片不处理
            if (image.closest('.ithome_super_player')) return;
            if (image.classList.contains('ruanmei-emoji') && image.classList.contains('emoji')) return;
            if (image.classList.contains('ithome_super_player')) return;
            if (image.parentNode.tagName.toLowerCase() === 'p' && image.parentNode.children.length === 1) return;
            if (image.width < 25 || image.height < 20) return;
            
            const p = document.createElement('p');
            p.style.textAlign = 'center';
            p.style.margin = '0';
            p.setAttribute('data-vmark', 'f5e8');
            image.parentNode.insertBefore(p, image);
            p.appendChild(image);
        });
    }

    // 函数：视频处理 - 圆角、边框
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

    // 函数：评论区圆角
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

    // 函数：移除首页信息流广告
    function removeAds() {
        document.querySelectorAll('div.bb.clearfix > div.fl > ul.bl > li').forEach(element => {
            if (element.querySelector('div.c > div.m:empty')) element.remove();
        });
    }

    // 函数：自动点击「加载更多」按钮
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

            // 监听DOM变化
            const mutationObserver = new MutationObserver(() => {
                const newLoadMoreButton = document.querySelector('a.more');
                if (newLoadMoreButton && !observer.observe(newLoadMoreButton)) {
                    observer.observe(newLoadMoreButton);
                }
            });

            mutationObserver.observe(document.body, { childList: true, subtree: true });
        }
    }

    // 函数：处理评论区图片
    function handleNewNodes(nodes) {
        nodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                if (node.matches('.post-img-list.c-1')) {
                    decodeAndDisplayImage(node);
                }
                node.querySelectorAll('.post-img-list.c-1').forEach((childNode) => {
                    decodeAndDisplayImage(childNode);
                });
            }
        });
    }

    // 函数：解码评论区图片
    function decodeAndDisplayImages(node) {
        try {
            const spanList = node.querySelectorAll('span.img-placeholder');
            spanList.forEach(span => {
                const dataS = span.getAttribute('data-s');
                if (dataS) {
                    let decodedUrl;
                    try {
                        decodedUrl = atob(dataS);
                    } catch (error) {
                        console.error("图片 URL 解码失败：", error, dataS);
                        return;
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

                    span.innerHTML = '';
                    span.appendChild(img);
                }
            });
        } catch (e) {
            console.error("处理图片时出错：", e, node);
        }
    }

    // 函数：观察DOM变化，处理新刷出的内容
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
                            if (node.matches('.post-img-list')) {
                                decodeAndDisplayImages(node);
                            }
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

    document.querySelectorAll('.post-img-list.c-1').forEach((node) => {
        decodeAndDisplayImage(node);
    });

    document.querySelectorAll('.post-img-list').forEach((node) => {
        decodeAndDisplayImages(node);
    });

    // 监听事件
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