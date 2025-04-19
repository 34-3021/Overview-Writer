## 如何为综述写作助手做贡献

### 1. 开始之前

- 阅读项目README和文档
- 确保你的开发环境配置正确（Python 3.9+/Node.js 16+）
- 查看 GitHub Issues 中的`good first issue`标签

### 2. 开发流程

1. **Fork 仓库**
   ```bash
   git clone https://github.com/your-username/Overview-Writer.git
   ```

2. **创建分支**
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. **提交变更**
   - 遵循[Conventional Commits](https://www.conventionalcommits.org/)规范
   - 示例：
     ```bash
     git commit -m "feat(editor): add markdown preview toggle"
     ```

4. **推送变更**
   ```bash
   git push origin feat/your-feature-name
   ```

### 3. 代码规范

- **前端**: 遵循 Nuxt3 和 ESLint 规则
- **后端**: 使用 Black 格式化 Python 代码
- **测试**: 新功能需包含单元测试
- **文档**: 重大变更需更新相关文档

### 4. 提交Pull Request

1. 确保你的分支与主分支保持同步
2. 提供清晰的PR描述，包括：
   - 变更目的
   - 测试方法
   - 屏幕截图（如适用）
3. 等待 CI 通过并处理 review 意见

### 5. 其他贡献方式

- 报告 Bug（提供复现步骤和环境信息）
- 建议新功能
- 改进文档
- 帮助解答社区问题
