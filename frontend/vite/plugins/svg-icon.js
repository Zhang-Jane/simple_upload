import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'




export default function createSvgIcon(isBuild) {
    return createSvgIconsPlugin({
		iconDirs: [path.resolve(process.cwd(), 'src/public/icons/')], // iconDirs: 指定存放 SVG 图标的目录。在这里，我们使用 path.resolve 来确保路径的正确性。
        symbolId: 'icon-[dir]-[name]', // symbolId: 定义生成的 SVG symbol 的 ID 格式。[dir] 和 [name] 会被替换为图标的目录名和文件名。
        svgoOptions: isBuild // svgoOptions: 在构建时启用 SVGO 优化选项，以减少 SVG 文件的大小。
    })
}
