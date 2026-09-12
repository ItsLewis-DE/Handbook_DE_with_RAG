(() => {
  // Coordinates follow the original 1282 × 810 photograph, including its cropped feet.
  const silhouette = 'M 551 810 C 546 787 548 756 555 729 L 565 680 L 571 635 L 564 632 L 562 649 L 554 664 L 540 660 L 535 647 L 532 621 L 531 601 C 530 579 540 546 548 519 L 563 473 C 573 445 592 434 628 425 L 628 408 C 621 391 625 371 633 360 L 642 350 L 648 355 L 655 345 L 660 353 L 666 346 L 669 355 C 688 353 697 368 696 383 L 688 410 L 684 430 C 708 434 726 443 732 464 L 745 510 L 754 552 L 764 602 L 762 636 L 760 653 L 747 664 L 738 662 L 732 645 L 733 625 L 720 586 L 709 550 L 704 585 L 699 625 L 702 654 L 704 703 C 709 748 701 784 685 810 L 634 810 L 634 774 L 635 719 L 631 687 L 627 728 C 625 771 610 798 605 810 Z';
  const ns = 'http://www.w3.org/2000/svg';

  function portrait(source, id, cropped = false) {
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', cropped ? '490 325 310 485' : '0 0 1282 810');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    svg.setAttribute('aria-hidden', 'true');
    svg.classList.add('author-character');
    const defs = document.createElementNS(ns, 'defs');
    const clip = document.createElementNS(ns, 'clipPath');
    clip.id = id;
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', silhouette);
    clip.append(path);
    defs.append(clip);
    const outline = path.cloneNode();
    outline.setAttribute('class', 'author-character__outline');
    const photo = document.createElementNS(ns, 'image');
    photo.setAttribute('href', source);
    photo.setAttribute('width', '1282');
    photo.setAttribute('height', '810');
    photo.setAttribute('clip-path', `url(#${id})`);
    svg.append(defs, outline, photo);
    return svg;
  }

  function initialise() {
    const frame = document.querySelector('.author-photo__frame');
    const photo = frame?.querySelector('img');
    if (!photo || frame.dataset.dialogReady) return;
    frame.dataset.dialogReady = 'true';

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'author-photo__trigger';
    trigger.setAttribute('aria-haspopup', 'dialog');
    trigger.setAttribute('aria-controls', 'author-dialog');
    trigger.setAttribute('aria-label', 'Nghe đôi lời từ Phong Thanh');
    trigger.append(portrait(photo.src, 'author-preview-clip'));
    const hint = document.createElement('span');
    hint.className = 'author-photo__hint';
    hint.textContent = 'Có chuyện muốn kể…';
    trigger.append(hint);
    frame.append(trigger);

    const dialog = document.createElement('dialog');
    dialog.id = 'author-dialog';
    dialog.className = 'author-dialog';
    dialog.setAttribute('aria-labelledby', 'author-dialog-title');
    dialog.setAttribute('aria-describedby', 'author-dialog-message');
    dialog.innerHTML = `
      <div class="author-dialog__scene">
        <button class="author-dialog__close" type="button" aria-label="Đóng lời nhắn" autofocus>×</button>
        <div class="author-dialog__portrait"></div>
        <div class="author-dialog__bubble">
          <p class="author-dialog__eyebrow">ĐÔI LỜI TỪ NGƯỜI VIẾT <span aria-hidden="true">01 /</span></p>
          <span class="author-dialog__spark" aria-hidden="true">✳</span>
          <h2 id="author-dialog-title">Chào cả nhà<span>!</span></h2>
          <div id="author-dialog-message">
            <p>Những bài viết ở đây là kiến thức mình ghi chép lại, để cả nhà và chính mình sau này đọc lại đều có thể <mark class="author-dialog__highlight">hiểu vững hơn</mark> những công cụ đang dùng.</p>
            <p>Có chỗ mình hiểu chưa đúng hoặc viết chưa chính xác. Nếu cả nhà có góp ý, cứ <span class="author-dialog__mail-hint">gửi mail cho mình nhé</span> — mình rất vui được học thêm từ mọi người!</p>
            <p class="author-dialog__thanks">Cảm ơn cả nhà đã ghé qua! <span class="author-dialog__wave" aria-hidden="true">👋</span></p>
          </div>
          <div class="author-dialog__signature"><span class="author-dialog__seal" aria-hidden="true"><span class="author-dialog__seal-text">PT</span><span class="author-dialog__seal-ring"></span></span><p>Phong Thanh <span>Học, làm, rồi ghi lại.</span></p><span class="author-dialog__end" aria-hidden="true">↗</span></div>
        </div>
      </div>`;
    dialog.querySelector('.author-dialog__portrait').append(portrait(photo.src, 'author-dialog-clip', true));
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialise, { once: true });
  } else {
    initialise();
  }
})();
