import { Node } from '../../models/node';
import { Point } from '../../models/point';
import { Direction } from '../../models/direction';

export function imageAnchors(node: Node) {
  const textHeight = node.text
    ? node.paddingBottomNum || node.font.lineHeight * node.font.fontSize * (node.textMaxLine || 1)
    : 0;

  node.anchors.push(new Point(node.rect.x, node.rect.y + (node.rect.height - textHeight) / 2, Direction.Left));
  node.anchors.push(new Point(node.rect.x + node.rect.width / 2, node.rect.y, Direction.Up));
  node.anchors.push(
    new Point(node.rect.x + node.rect.width, node.rect.y + (node.rect.height - textHeight) / 2, Direction.Right)
  );
  node.anchors.push(
    new Point(node.rect.x + node.rect.width / 2, node.rect.y + node.rect.height - textHeight, Direction.Bottom)
  );
}
