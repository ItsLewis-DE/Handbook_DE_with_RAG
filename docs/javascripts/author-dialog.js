(() => {
  // Coordinates follow the original 1282 × 810 photograph, including its cropped feet.
  const silhouette = 'M 551 810 C 546 787 548 756 555 729 L 565 680 L 571 635 L 564 632 L 562 649 L 554 664 L 540 660 L 535 647 L 532 621 L 531 601 C 530 579 540 546 548 519 L 563 473 C 573 445 592 434 628 425 L 628 408 C 621 391 625 371 633 360 L 642 350 L 648 355 L 655 345 L 660 353 L 666 346 L 669 355 C 688 353 697 368 696 383 L 688 410 L 684 430 C 708 434 726 443 732 464 L 745 510 L 754 552 L 764 602 L 762 636 L 760 653 L 747 664 L 738 662 L 732 645 L 733 625 L 720 586 L 709 550 L 704 585 L 699 625 L 702 654 L 704 703 C 709 748 701 784 685 810 L 634 810 L 634 774 L 635 719 L 631 687 L 627 728 C 625 771 610 798 605 810 Z';
  const ns = 'http://www.w3.org/2000/svg';

  const authors = [
    { id: 'author', name: 'Phong Thanh', frame: '.author-photo__frame', silhouette,
      width: 1282, height: 810, crop: '490 325 310 485', aspect: '310 / 485' },
    { id: 'coauthor', name: 'Danh', frame: '.coauthor-card__photo-frame',
      width: 460, height: 460, crop: '65 10 300 450', aspect: '300 / 450',
      silhouette: 'M 146 470 L 147 449 C 124 438 115 419 112 398 L 97 401 L 87 379 L 88 363 C 77 336 83 297 88 266 L 98 220 C 104 196 119 181 145 174 L 188 159 L 193 147 L 190 129 C 177 127 173 109 177 99 C 169 79 174 59 187 47 C 195 39 200 30 215 27 L 233 21 L 229 27 C 253 24 265 43 266 58 C 274 75 270 85 266 94 C 277 97 269 115 260 120 L 255 147 L 261 167 C 280 176 310 185 319 206 C 331 239 334 282 339 323 L 346 381 L 353 392 L 349 420 L 335 429 L 340 460 L 344 470 Z' },
  ];

  function portrait(source, id, author, cropped = false) {
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', cropped ? author.crop : `0 0 ${author.width} ${author.height}`);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    svg.setAttribute('aria-hidden', 'true');
    svg.classList.add('author-character');
    const defs = document.createElementNS(ns, 'defs');
    const clip = document.createElementNS(ns, 'clipPath');
    clip.id = id;
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', author.silhouette);
    clip.append(path);
    defs.append(clip);
    const outline = path.cloneNode();
    outline.setAttribute('class', 'author-character__outline');
    const photo = document.createElementNS(ns, 'image');
    photo.setAttribute('href', source);
    photo.setAttribute('width', author.width);
    photo.setAttribute('height', author.height);
    photo.setAttribute('clip-path', `url(#${id})`);
    svg.append(defs, outline, photo);
    return svg;
  }

  function initialiseAuthor(author) {
    const frame = document.querySelector(author.frame);
    const photo = frame?.querySelector('img');
    if (!photo || frame.dataset.dialogReady) return;
    frame.dataset.dialogReady = 'true';

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'author-photo__trigger';
    trigger.setAttribute('aria-haspopup', 'dialog');
    trigger.setAttribute('aria-controls', `${author.id}-dialog`);
    trigger.setAttribute('aria-label', `Nghe đôi lời từ ${author.name}`);
    trigger.append(portrait(photo.src, `${author.id}-preview-clip`, author));
    const hint = document.createElement('span');
    hint.className = 'author-photo__hint';
    hint.textContent = author.id === 'coauthor' ? 'Danh cũng có lời nhắn…' : 'Có chuyện muốn kể…';
    trigger.append(hint);
    frame.append(trigger);

    const dialog = document.createElement('dialog');
    dialog.id = `${author.id}-dialog`;
    dialog.dataset.author = author.id;
    dialog.className = 'author-dialog';
    dialog.setAttribute('aria-labelledby', `${author.id}-dialog-title`);
    dialog.setAttribute('aria-describedby', `${author.id}-dialog-message`);
    dialog.innerHTML = `
      <div class="author-dialog__scene">
        <button class="author-dialog__close" type="button" aria-label="Đóng lời nhắn" autofocus>×</button>
        <div class="author-dialog__portrait"></div>
        <div class="author-dialog__bubble">
          <p class="author-dialog__eyebrow">ĐÔI LỜI TỪ NGƯỜI VIẾT <span aria-hidden="true">01 /</span></p>
          <span class="author-dialog__spark" aria-hidden="true">✳</span>
          <h2 id="${author.id}-dialog-title">Chào cả nhà<span>!</span></h2>
          <div id="${author.id}-dialog-message" class="author-dialog__message">
            <p>Những bài viết ở đây là kiến thức mình ghi chép lại, để cả nhà và chính mình sau này đọc lại đều có thể <mark class="author-dialog__highlight">hiểu vững hơn</mark> những công cụ đang dùng.</p>
            <p>Có chỗ mình hiểu chưa đúng hoặc viết chưa chính xác. Nếu cả nhà có góp ý, cứ <span class="author-dialog__mail-hint">gửi mail cho mình nhé</span> — mình rất vui được học thêm từ mọi người!</p>
            <p class="author-dialog__thanks">Cảm ơn cả nhà đã ghé qua! <span class="author-dialog__wave" aria-hidden="true">👋</span></p>
          </div>
          <div class="author-dialog__signature"><span class="author-dialog__seal" aria-hidden="true"><span class="author-dialog__seal-text">PT</span><span class="author-dialog__seal-ring"></span></span><p>Phong Thanh <span>Học, làm, rồi ghi lại.</span></p><span class="author-dialog__end" aria-hidden="true">↗</span></div>
        </div>
      </div>`;
    if (author.id === 'coauthor') {
      dialog.querySelector('.author-dialog__eyebrow').textContent = 'ĐÔI LỜI TỪ ĐỒNG TÁC GIẢ';
      dialog.querySelector('h2').innerHTML = 'Danh chào bạn<span>!</span>';
      dialog.querySelector('.author-dialog__message').innerHTML = `
        <p>Mình là Danh, cùng góp một góc nhìn cho Behind the Pipeline. Mình thích đi từ những câu hỏi nhỏ, thử lại từng ý và tìm cách giải thích để kiến thức <mark class="author-dialog__highlight">dễ hiểu hơn một chút</mark>.</p>
        <p>Hy vọng những ghi chép này giúp bạn nối được điều đang đọc với điều đang làm. Nếu có chỗ còn khó hiểu hoặc bạn có cách nhìn khác, cứ chia sẻ với tụi mình nhé!</p>
        <p class="author-dialog__thanks">Cảm ơn bạn đã ghé đọc và học cùng tụi mình! <span class="author-dialog__wave" aria-hidden="true">👋</span></p>`;
      dialog.querySelector('.author-dialog__seal-text').textContent = 'D';
      dialog.querySelector('.author-dialog__signature p').innerHTML = 'Danh <span>Cùng đọc, cùng viết, cùng hiểu thêm.</span>';
    }
    const portraitFrame = dialog.querySelector('.author-dialog__portrait');
    portraitFrame.style.aspectRatio = author.aspect;
    portraitFrame.append(portrait(photo.src, `${author.id}-dialog-clip`, author, true));
    document.body.append(dialog);

    trigger.addEventListener('click', () => {
      dialog.showModal();
      document.documentElement.classList.add('author-dialog-open');
    });
    dialog.querySelector('.author-dialog__close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('keydown', (event) => {
      // This dialog has one focusable control; keep Tab and Shift+Tab on it.
      if (event.key === 'Tab') {
        event.preventDefault();
        dialog.querySelector('.author-dialog__close').focus();
      }
    });
    // Only close when both ends of the gesture land outside the scene.
    let backdropPress = false;
    dialog.addEventListener('pointerdown', (event) => { backdropPress = event.target === dialog; });
    dialog.addEventListener('click', (event) => {
      if (backdropPress && event.target === dialog) dialog.close();
      backdropPress = false;
    });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('author-dialog-open');
      trigger.focus({ preventScroll: true });
    });
  }

  function initialise() {
    authors.forEach(initialiseAuthor);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialise, { once: true });
  } else {
    initialise();
  }
})();
