class Star {
    constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.size = 0.5;
    }

    update(width, height, speed) {
        this.z -= speed;
        if (this.z <= 0) {
            this.z = width;
            this.x = Math.random() * width - width / 2;
            this.y = Math.random() * height - height / 2;
        }
    }

    draw(ctx, width, height) {
        let x = this.x / this.z * width + width / 2;
        let y = this.y / this.z * height + height / 2;
        let s = this.size * (width / this.z);

        ctx.beginPath();
        ctx.fillStyle = "#ffffff";
        ctx.arc(x, y, s, 0, 2 * Math.PI);
        ctx.fill();
    }
}

const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

let width = canvas.width = window.innerWidth;
let height = canvas.height = window.innerHeight;

const stars = [];
const starCount = 1000;
const speed = 2;

for (let i = 0; i < starCount; i++) {
    stars.push(new Star(
        Math.random() * width - width / 2,
        Math.random() * height - height / 2,
        Math.random() * width
    ));
}

function animate() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, width, height);

    stars.forEach(star => {
        star.update(width, height, speed);
        star.draw(ctx, width, height);
    });

    requestAnimationFrame(animate);
}

window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
});

animate();