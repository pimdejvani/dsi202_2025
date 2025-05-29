document.addEventListener("DOMContentLoaded", function () {
  const MONTHS_TH = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
  ];

  function formatThaiDate(dateStr) {
    try {
      const date = new Date(dateStr);
      if (isNaN(date)) throw new Error("Invalid date");
      const day = date.getDate();
      const month = MONTHS_TH[date.getMonth()];
      const year = date.getFullYear();
      return `${day} ${month} ${year}`;
    } catch {
      return "วันที่ไม่ถูกต้อง";
    }
  }

  function getDaysUntil(dateStr) {
    try {
      const today = new Date();
      const target = new Date(dateStr);
      if (isNaN(target)) throw new Error("Invalid date");
      const diffTime = target - today;
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    } catch {
      return NaN;
    }
  }

  function getStatusAndColor(daysUntil) {
    if (isNaN(daysUntil)) return { status: "วันที่ไม่ถูกต้อง", color: "#808080" }; // Gray for invalid dates
    if (daysUntil < 0) return { status: "ปิดรับสมัคร", color: "#000000" };
    if (daysUntil === 0) return { status: "รับสมัครวันสุดท้าย", color: "#CD4236" };
    if (daysUntil === 1) return { status: "รับสมัครภายใน 1 วัน", color: "#E8553E" };
    if (daysUntil === 2) return { status: "รับสมัครภายใน 2 วัน", color: "#F47C48" };
    if (daysUntil === 3) return { status: "รับสมัครภายใน 3 วัน", color: "#FBB061" };
    if (daysUntil <= 6) return { status: "รับสมัครภายในสัปดาห์นี้", color: "#FFD27A" };
    return { status: "เปิดรับสมัครอยู่", color: "#255681" };
  }

  document.querySelectorAll('.camp-item').forEach(item => {
    const finalDate = item.dataset.finalDate;
    const days = getDaysUntil(finalDate);
    const { status, color } = getStatusAndColor(days);

    // Update status text
    const statusElement = item.querySelector('.status-value');
    if (statusElement) {
      statusElement.textContent = status;
      // Optional: Style status text based on status
      statusElement.style.color = "#FFFFFF";
    }

    // Update color indicator
    const colorElement = item.querySelector('.color-indicator');
    if (colorElement) {
      colorElement.style.backgroundColor = color;
    }
  });
});