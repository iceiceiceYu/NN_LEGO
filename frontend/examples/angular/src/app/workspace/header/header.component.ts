import { Component, OnInit, Input, OnDestroy, Output, EventEmitter } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { Store } from 'le5le-store';

@Component({
  selector: 'app-workspace-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  host: {
    '(document:onscroll)': 'onscroll($event)'
  }
})
export class WorkspaceHeaderComponent implements OnInit, OnDestroy {
  @Input() file: any;
  @Input() data: any;

  @Output() event = new EventEmitter<any>();

  user: any;
  subUser: any;

  menuClicked = false;
  showFigure = false;
  bkTab = 1;
  recently: any[] = [];

  dialogs: any = {};

  lineNames = [{
    name: '曲线',
    value: 'curve'
  }, {
    name: '线段',
    value: 'polyline'
  }, {
    name: '直线',
    value: 'line'
  }, {
    name: '脑图曲线',
    value: 'mind'
  }];
  arrowTypes = [
    '',
    'triangleSolid',
    'triangle',
    'diamondSolid',
    'diamond',
    'circleSolid',
    'circle',
    'line',
    'lineUp',
    'lineDown'
  ];

  menus: any[] = [];

  cpPresetColors = [
    '#1890ff',
    '#096dd9',
    '#bae7ff',
    '#52c41a',
    '#3fad09',
    '#c6ebb4',
    '#faad14',
    '#d9a116',
    '#fff6dd',
    '#f50000',
    '#ff0000',
    '#ffc2c5',
    '#fa541c',
    '#531dab',
    '#314659',
    '#777777'
  ];

  id: string;
  subRoute: any;
  subRecently: any;
  constructor(private router: Router, private activateRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.subUser = Store.subscribe('user', (user: any) => {
      this.user = user;
      this.getRecently();
    });

    this.subRoute = this.activateRoute.queryParamMap.subscribe(params => {
      this.id = params.get('id');
    });

    setTimeout(() => {
      this.subRecently = Store.subscribe('recently', (item: any) => {
        if (!item) {
          return;
        }
        for (let i = 0; i < this.recently.length; ++i) {
          if (this.recently[i].id === item.id || i > 19) {
            this.recently.splice(i, 1);
          }
        }
        this.recently.unshift(item);
        if (this.user) {
          localStorage.setItem('recently_' + this.user.id, JSON.stringify(this.recently));
        } else {
          localStorage.setItem('recently_local', JSON.stringify(this.recently));
        }
      });
    }, 500);
  }

  onRemoveRecently(event: MouseEvent, i: number) {
    event.stopPropagation();
    event.preventDefault();
    this.recently.splice(i, 1);
    if (this.user) {
      localStorage.setItem('recently_' + this.user.id, JSON.stringify(this.recently));
    } else {
      localStorage.setItem('recently_local', JSON.stringify(this.recently));
    }
  }

  getRecently() {
    try {
      if (this.user) {
        this.recently = JSON.parse(localStorage.getItem('recently_' + this.user.id));
      } else {
        this.recently = JSON.parse(localStorage.getItem('recently_local'));
      }
    } catch (e) { }
    if (!this.recently) {
      this.recently = [];
    }
  }

  onMenu(name: string, data?: any) {
    this.event.emit({
      name,
      data
    });
  }


  onClickMenu(event: MouseEvent) {
    if ((event.target as HTMLElement).nodeName === 'A') {
      let node = (event.target as HTMLElement).parentElement;
      let isDropdown = false;
      let disabled = false;
      while (node) {
        if (node.className.indexOf('dropdown') > -1) {
          isDropdown = true;
        }
        if (node.className.indexOf('disabled') > -1) {
          disabled = true;
          break;
        }
        node = node.parentElement;
      }

      if (disabled) {
        return;
      }
    }

    this.menuClicked = true;
    setTimeout(() => {
      this.menuClicked = false;
    }, 500);
  }

  onLeaveFigure() {
    setTimeout(() => {
      this.showFigure = false;
    }, 1000);
  }

  ngOnDestroy() {
    this.subUser.unsubscribe();
    this.subRoute.unsubscribe();
    this.subRecently.unsubscribe();
  }
}
