import { Node } from '../../models/node';
import { Rect } from '../../models/rect';

export function imageIconRect(node: Node) {
  const textHeight = node.text
    ? node.paddingBottomNum || node.font.lineHeight * node.font.fontSize * (node.textMaxLine || 1)
    : 0;

  node.iconRect = new Rect(node.rect.x, node.rect.y, node.rect.width, node.rect.height - textHeight);
  node.fullIconRect = node.rect;
}

export function imageTextRect(node: Node) {
  const height = node.paddingBottomNum || node.font.lineHeight * node.font.fontSize * (node.textMaxLine || 1);
  node.textRect = new Rect(
    node.rect.x,
    node.rect.y + node.rect.height - height,
    node.rect.width - node.textOffsetX * 2,
    height
  );
  node.fullTextRect = node.rect;
}
