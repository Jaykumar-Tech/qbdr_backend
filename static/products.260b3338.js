import{a as ne,g as te,s as N,_ as c,r as h,u as xe,b as K,a1 as Je,a2 as Ye,j as n,c as T,d as se,U as re,a3 as Ie,a4 as Qe,m as D,a5 as eo,a6 as oo,a7 as Ne,a8 as Pe,a9 as me,aa as no,ab as to,ac as so,ad as ro,E as ue,S as y,V as ao,t as oe,f as _,P as x,B as q,T as I,C as io,L as lo,k as fe,ae as co,af as uo,M as po,F as ee,e as ho,ag as fo,I as xo,D as mo,i as go,ah as vo,A as bo,G as Ce,W as yo}from"./main.051f1dba.js";import{l as Co,L as jo}from"./label.78eda6e1.js";import{b as je}from"./format-number.ba0353bf.js";import{v as Ro}from"./visuallyHidden.fa9934b5.js";function Fo(e){return ne("MuiFormGroup",e)}te("MuiFormGroup",["root","row","error"]);const So=["className","row"],wo=e=>{const{classes:o,row:t,error:s}=e;return se({root:["root",t&&"row",s&&"error"]},Fo,o)},ko=N("div",{name:"MuiFormGroup",slot:"Root",overridesResolver:(e,o)=>{const{ownerState:t}=e;return[o.root,t.row&&o.row]}})(({ownerState:e})=>c({display:"flex",flexDirection:"column",flexWrap:"wrap"},e.row&&{flexDirection:"row"})),Io=h.forwardRef(function(o,t){const s=xe({props:o,name:"MuiFormGroup"}),{className:r,row:u=!1}=s,f=K(s,So),d=Je(),a=Ye({props:s,muiFormControl:d,states:["error"]}),i=c({},s,{row:u,error:a.error}),v=wo(i);return n.jsx(ko,c({className:T(v.root,r),ownerState:i,ref:t},f))}),Ae=Io,No=re(n.jsx("path",{d:"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"}),"RadioButtonUnchecked"),Po=re(n.jsx("path",{d:"M8.465 8.465C9.37 7.56 10.62 7 12 7C14.76 7 17 9.24 17 12C17 13.38 16.44 14.63 15.535 15.535C14.63 16.44 13.38 17 12 17C9.24 17 7 14.76 7 12C7 10.62 7.56 9.37 8.465 8.465Z"}),"RadioButtonChecked"),Ao=N("span",{shouldForwardProp:Ie})({position:"relative",display:"flex"}),Oo=N(No)({transform:"scale(1)"}),$o=N(Po)(({theme:e,ownerState:o})=>c({left:0,position:"absolute",transform:"scale(0)",transition:e.transitions.create("transform",{easing:e.transitions.easing.easeIn,duration:e.transitions.duration.shortest})},o.checked&&{transform:"scale(1)",transition:e.transitions.create("transform",{easing:e.transitions.easing.easeOut,duration:e.transitions.duration.shortest})}));function Oe(e){const{checked:o=!1,classes:t={},fontSize:s}=e,r=c({},e,{checked:o});return n.jsxs(Ao,{className:t.root,ownerState:r,children:[n.jsx(Oo,{fontSize:s,className:t.background,ownerState:r}),n.jsx($o,{fontSize:s,className:t.dot,ownerState:r})]})}const Mo=h.createContext(void 0),$e=Mo;function zo(){return h.useContext($e)}function Vo(e){return ne("MuiRadio",e)}const To=te("MuiRadio",["root","checked","disabled","colorPrimary","colorSecondary","sizeSmall"]),Re=To,Bo=["checked","checkedIcon","color","icon","name","onChange","size","className"],Eo=e=>{const{classes:o,color:t,size:s}=e,r={root:["root",`color${D(t)}`,s!=="medium"&&`size${D(s)}`]};return c({},o,se(r,Vo,o))},Lo=N(Qe,{shouldForwardProp:e=>Ie(e)||e==="classes",name:"MuiRadio",slot:"Root",overridesResolver:(e,o)=>{const{ownerState:t}=e;return[o.root,t.size!=="medium"&&o[`size${D(t.size)}`],o[`color${D(t.color)}`]]}})(({theme:e,ownerState:o})=>c({color:(e.vars||e).palette.text.secondary},!o.disableRipple&&{"&:hover":{backgroundColor:e.vars?`rgba(${o.color==="default"?e.vars.palette.action.activeChannel:e.vars.palette[o.color].mainChannel} / ${e.vars.palette.action.hoverOpacity})`:eo(o.color==="default"?e.palette.action.active:e.palette[o.color].main,e.palette.action.hoverOpacity),"@media (hover: none)":{backgroundColor:"transparent"}}},o.color!=="default"&&{[`&.${Re.checked}`]:{color:(e.vars||e).palette[o.color].main}},{[`&.${Re.disabled}`]:{color:(e.vars||e).palette.action.disabled}}));function Go(e,o){return typeof o=="object"&&o!==null?e===o:String(e)===String(o)}const Fe=n.jsx(Oe,{checked:!0}),Se=n.jsx(Oe,{}),Ho=h.forwardRef(function(o,t){var s,r;const u=xe({props:o,name:"MuiRadio"}),{checked:f,checkedIcon:d=Fe,color:a="primary",icon:i=Se,name:v,onChange:l,size:F="medium",className:S}=u,O=K(u,Bo),w=c({},u,{color:a,size:F}),j=Eo(w),R=zo();let m=f;const b=oo(l,R&&R.onChange);let C=v;return R&&(typeof m>"u"&&(m=Go(R.value,u.value)),typeof C>"u"&&(C=R.name)),n.jsx(Lo,c({type:"radio",icon:h.cloneElement(i,{fontSize:(s=Se.props.fontSize)!=null?s:F}),checkedIcon:h.cloneElement(d,{fontSize:(r=Fe.props.fontSize)!=null?r:F}),ownerState:w,classes:j,name:C,checked:m,onChange:b,ref:t,className:T(j.root,S)},O))}),de=Ho;function _o(e){return ne("MuiRadioGroup",e)}te("MuiRadioGroup",["root","row","error"]);const Do=["actions","children","className","defaultValue","name","onChange","value"],Uo=e=>{const{classes:o,row:t,error:s}=e;return se({root:["root",t&&"row",s&&"error"]},_o,o)},Wo=h.forwardRef(function(o,t){const{actions:s,children:r,className:u,defaultValue:f,name:d,onChange:a,value:i}=o,v=K(o,Do),l=h.useRef(null),F=Uo(o),[S,O]=Ne({controlled:i,default:f,name:"RadioGroup"});h.useImperativeHandle(s,()=>({focus:()=>{let m=l.current.querySelector("input:not(:disabled):checked");m||(m=l.current.querySelector("input:not(:disabled)")),m&&m.focus()}}),[]);const w=Pe(t,l),j=me(d),R=h.useMemo(()=>({name:j,onChange(m){O(m.target.value),a&&a(m,m.target.value)},value:S}),[j,a,O,S]);return n.jsx($e.Provider,{value:R,children:n.jsx(Ae,c({role:"radiogroup",ref:w,className:T(F.root,u)},v,{children:r}))})}),pe=Wo,Xo=re(n.jsx("path",{d:"M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"}),"Star"),Zo=re(n.jsx("path",{d:"M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z"}),"StarBorder");function qo(e){return ne("MuiRating",e)}const Ko=te("MuiRating",["root","sizeSmall","sizeMedium","sizeLarge","readOnly","disabled","focusVisible","visuallyHidden","pristine","label","labelEmptyValueActive","icon","iconEmpty","iconFilled","iconHover","iconFocus","iconActive","decimal"]),Z=Ko,Jo=["value"],Yo=["className","defaultValue","disabled","emptyIcon","emptyLabelText","getLabelText","highlightSelectedOnly","icon","IconContainerComponent","max","name","onChange","onChangeActive","onMouseLeave","onMouseMove","precision","readOnly","size","value"];function Qo(e){const o=e.toString().split(".")[1];return o?o.length:0}function he(e,o){if(e==null)return e;const t=Math.round(e/o)*o;return Number(t.toFixed(Qo(o)))}const en=e=>{const{classes:o,size:t,readOnly:s,disabled:r,emptyValueFocused:u,focusVisible:f}=e,d={root:["root",`size${D(t)}`,r&&"disabled",f&&"focusVisible",s&&"readOnly"],label:["label","pristine"],labelEmptyValue:[u&&"labelEmptyValueActive"],icon:["icon"],iconEmpty:["iconEmpty"],iconFilled:["iconFilled"],iconHover:["iconHover"],iconFocus:["iconFocus"],iconActive:["iconActive"],decimal:["decimal"],visuallyHidden:["visuallyHidden"]};return se(d,qo,o)},on=N("span",{name:"MuiRating",slot:"Root",overridesResolver:(e,o)=>{const{ownerState:t}=e;return[{[`& .${Z.visuallyHidden}`]:o.visuallyHidden},o.root,o[`size${D(t.size)}`],t.readOnly&&o.readOnly]}})(({theme:e,ownerState:o})=>c({display:"inline-flex",position:"relative",fontSize:e.typography.pxToRem(24),color:"#faaf00",cursor:"pointer",textAlign:"left",width:"min-content",WebkitTapHighlightColor:"transparent",[`&.${Z.disabled}`]:{opacity:(e.vars||e).palette.action.disabledOpacity,pointerEvents:"none"},[`&.${Z.focusVisible} .${Z.iconActive}`]:{outline:"1px solid #999"},[`& .${Z.visuallyHidden}`]:Ro},o.size==="small"&&{fontSize:e.typography.pxToRem(18)},o.size==="large"&&{fontSize:e.typography.pxToRem(30)},o.readOnly&&{pointerEvents:"none"})),Me=N("label",{name:"MuiRating",slot:"Label",overridesResolver:({ownerState:e},o)=>[o.label,e.emptyValueFocused&&o.labelEmptyValueActive]})(({ownerState:e})=>c({cursor:"inherit"},e.emptyValueFocused&&{top:0,bottom:0,position:"absolute",outline:"1px solid #999",width:"100%"})),nn=N("span",{name:"MuiRating",slot:"Icon",overridesResolver:(e,o)=>{const{ownerState:t}=e;return[o.icon,t.iconEmpty&&o.iconEmpty,t.iconFilled&&o.iconFilled,t.iconHover&&o.iconHover,t.iconFocus&&o.iconFocus,t.iconActive&&o.iconActive]}})(({theme:e,ownerState:o})=>c({display:"flex",transition:e.transitions.create("transform",{duration:e.transitions.duration.shortest}),pointerEvents:"none"},o.iconActive&&{transform:"scale(1.2)"},o.iconEmpty&&{color:(e.vars||e).palette.action.disabled})),tn=N("span",{name:"MuiRating",slot:"Decimal",shouldForwardProp:e=>no(e)&&e!=="iconActive",overridesResolver:(e,o)=>{const{iconActive:t}=e;return[o.decimal,t&&o.iconActive]}})(({iconActive:e})=>c({position:"relative"},e&&{transform:"scale(1.2)"}));function sn(e){const o=K(e,Jo);return n.jsx("span",c({},o))}function we(e){const{classes:o,disabled:t,emptyIcon:s,focus:r,getLabelText:u,highlightSelectedOnly:f,hover:d,icon:a,IconContainerComponent:i,isActive:v,itemValue:l,labelProps:F,name:S,onBlur:O,onChange:w,onClick:j,onFocus:R,readOnly:m,ownerState:b,ratingValue:C,ratingValueRounded:ae}=e,B=f?l===C:l<=C,J=l<=d,E=l<=r,ie=l===ae,U=me(),M=n.jsx(nn,{as:i,value:l,className:T(o.icon,B?o.iconFilled:o.iconEmpty,J&&o.iconHover,E&&o.iconFocus,v&&o.iconActive),ownerState:c({},b,{iconEmpty:!B,iconFilled:B,iconHover:J,iconFocus:E,iconActive:v}),children:s&&!B?s:a});return m?n.jsx("span",c({},F,{children:M})):n.jsxs(h.Fragment,{children:[n.jsxs(Me,c({ownerState:c({},b,{emptyValueFocused:void 0}),htmlFor:U},F,{children:[M,n.jsx("span",{className:o.visuallyHidden,children:u(l)})]})),n.jsx("input",{className:o.visuallyHidden,onFocus:R,onBlur:O,onChange:w,onClick:j,disabled:t,value:l,id:U,type:"radio",name:S,checked:ie})]})}const rn=n.jsx(Xo,{fontSize:"inherit"}),an=n.jsx(Zo,{fontSize:"inherit"});function ln(e){return`${e} Star${e!==1?"s":""}`}const cn=h.forwardRef(function(o,t){const s=xe({name:"MuiRating",props:o}),{className:r,defaultValue:u=null,disabled:f=!1,emptyIcon:d=an,emptyLabelText:a="Empty",getLabelText:i=ln,highlightSelectedOnly:v=!1,icon:l=rn,IconContainerComponent:F=sn,max:S=5,name:O,onChange:w,onChangeActive:j,onMouseLeave:R,onMouseMove:m,precision:b=1,readOnly:C=!1,size:ae="medium",value:B}=s,J=K(s,Yo),E=me(O),[ie,U]=Ne({controlled:B,default:u,name:"Rating"}),M=he(ie,b),Ee=to(),[{hover:P,focus:Y},W]=h.useState({hover:-1,focus:-1});let L=M;P!==-1&&(L=P),Y!==-1&&(L=Y);const{isFocusVisibleRef:ge,onBlur:Le,onFocus:Ge,ref:He}=so(),[_e,le]=h.useState(!1),ve=h.useRef(),De=Pe(He,ve,t),Ue=p=>{m&&m(p);const g=ve.current,{right:k,left:Q,width:G}=g.getBoundingClientRect();let H;Ee?H=(k-p.clientX)/G:H=(p.clientX-Q)/G;let A=he(S*H+b/2,b);A=ro(A,b,S),W(z=>z.hover===A&&z.focus===A?z:{hover:A,focus:A}),le(!1),j&&P!==A&&j(p,A)},We=p=>{R&&R(p);const g=-1;W({hover:g,focus:g}),j&&P!==g&&j(p,g)},be=p=>{let g=p.target.value===""?null:parseFloat(p.target.value);P!==-1&&(g=P),U(g),w&&w(p,g)},Xe=p=>{p.clientX===0&&p.clientY===0||(W({hover:-1,focus:-1}),U(null),w&&parseFloat(p.target.value)===M&&w(p,null))},Ze=p=>{Ge(p),ge.current===!0&&le(!0);const g=parseFloat(p.target.value);W(k=>({hover:k.hover,focus:g}))},qe=p=>{if(P!==-1)return;Le(p),ge.current===!1&&le(!1);const g=-1;W(k=>({hover:k.hover,focus:g}))},[Ke,ye]=h.useState(!1),X=c({},s,{defaultValue:u,disabled:f,emptyIcon:d,emptyLabelText:a,emptyValueFocused:Ke,focusVisible:_e,getLabelText:i,icon:l,IconContainerComponent:F,max:S,precision:b,readOnly:C,size:ae}),$=en(X);return n.jsxs(on,c({ref:De,onMouseMove:Ue,onMouseLeave:We,className:T($.root,r,C&&"MuiRating-readOnly"),ownerState:X,role:C?"img":null,"aria-label":C?i(L):null},J,{children:[Array.from(new Array(S)).map((p,g)=>{const k=g+1,Q={classes:$,disabled:f,emptyIcon:d,focus:Y,getLabelText:i,highlightSelectedOnly:v,hover:P,icon:l,IconContainerComponent:F,name:E,onBlur:qe,onChange:be,onClick:Xe,onFocus:Ze,ratingValue:L,ratingValueRounded:M,readOnly:C,ownerState:X},G=k===Math.ceil(L)&&(P!==-1||Y!==-1);if(b<1){const H=Array.from(new Array(1/b));return n.jsx(tn,{className:T($.decimal,G&&$.iconActive),ownerState:X,iconActive:G,children:H.map((A,z)=>{const ce=he(k-1+(z+1)*b,b);return n.jsx(we,c({},Q,{isActive:!1,itemValue:ce,labelProps:{style:H.length-1===z?{}:{width:ce===L?`${(z+1)*b*100}%`:"0%",overflow:"hidden",position:"absolute"}}}),ce)})},k)}return n.jsx(we,c({},Q,{isActive:G,itemValue:k}),k)}),!C&&!f&&n.jsxs(Me,{className:T($.label,$.labelEmptyValue),ownerState:X,children:[n.jsx("input",{className:$.visuallyHidden,value:"",id:`${E}-empty`,type:"radio",name:E,checked:M==null,onFocus:()=>ye(!0),onBlur:()=>ye(!1),onChange:be}),n.jsx("span",{className:$.visuallyHidden,children:a})]})]}))}),ke=cn,un=["Nike Air Force 1 NDESTRUKT","Nike Space Hippie 04","Nike Air Zoom Pegasus 37 A.I.R. Chaz Bear","Nike Blazer Low 77 Vintage","Nike ZoomX SuperRep Surge","Zoom Freak 2","Nike Air Max Zephyr","Jordan Delta","Air Jordan XXXV PF","Nike Waffle Racer Crater","Kyrie 7 EP Sisterhood","Nike Air Zoom BB NXT","Nike Air Force 1 07 LX","Nike Air Force 1 Shadow SE","Nike Air Zoom Tempo NEXT%","Nike DBreak-Type","Nike Air Max Up","Nike Air Max 270 React ENG","NikeCourt Royale","Nike Air Zoom Pegasus 37 Premium","Nike Air Zoom SuperRep","NikeCourt Royale","Nike React Art3mis","Nike React Infinity Run Flyknit A.I.R. Chaz Bear"],V=["#00AB55","#000000","#FFFFFF","#FFC0CB","#FF4842","#1890FF","#94D82D","#FFC107"],dn=[...Array(24)].map((e,o)=>{const t=o+1;return{id:ue.string.uuid(),cover:`/static/assets/images/products/product_${t}.jpg`,name:un[o],price:ue.number.int({min:4,max:99,precision:.01}),priceSale:t%3?null:ue.number.int({min:19,max:29,precision:.01}),colors:t===1&&V.slice(0,2)||t===2&&V.slice(1,3)||t===3&&V.slice(2,4)||t===4&&V.slice(3,6)||t===23&&V.slice(4,6)||t===24&&V.slice(5,6)||V,status:Co.sample(["sale","new","",""])}}),ze=h.forwardRef(({colors:e,selected:o,onSelectColor:t,limit:s="auto",sx:r,...u},f)=>{const d=typeof o=="string",a=h.useCallback(i=>{if(d)i!==o&&t(i);else{const v=o.includes(i)?o.filter(l=>l!==i):[...o,i];t(v)}},[t,o,d]);return n.jsx(y,{ref:f,direction:"row",display:"inline-flex",sx:{flexWrap:"wrap",...s!=="auto"&&{width:s*36,justifyContent:"flex-end"},...r},...u,children:e.map(i=>{const v=d?o===i:o.includes(i);return n.jsx(ao,{sx:{width:36,height:36,borderRadius:"50%"},onClick:()=>{a(i)},children:n.jsx(y,{alignItems:"center",justifyContent:"center",sx:{width:20,height:20,bgcolor:i,borderRadius:"50%",border:l=>`solid 1px ${oe(l.palette.grey[500],.16)}`,...v&&{transform:"scale(1.3)",boxShadow:`4px 4px 8px 0 ${oe(i,.48)}`,outline:`solid 2px ${oe(i,.08)}`,transition:l=>l.transitions.create("all",{duration:l.transitions.duration.shortest})}},children:n.jsx(_,{width:v?12:0,icon:"eva:checkmark-fill",sx:{color:l=>l.palette.getContrastText(i),transition:l=>l.transitions.create("all",{duration:l.transitions.duration.shortest})}})})},i)})})});ze.propTypes={colors:x.oneOfType([x.string,x.arrayOf(x.string)]),limit:x.number,onSelectColor:x.func,selected:x.oneOfType([x.string,x.arrayOf(x.string)]),sx:x.object};const pn=ze;function Ve({colors:e,limit:o=3,sx:t}){const s=e.slice(0,o),r=e.length-o;return n.jsxs(y,{component:"span",direction:"row",alignItems:"center",justifyContent:"flex-end",sx:t,children:[s.map((u,f)=>n.jsx(q,{sx:{ml:-.75,width:16,height:16,bgcolor:u,borderRadius:"50%",border:d=>`solid 2px ${d.palette.background.paper}`,boxShadow:d=>`inset -1px 1px 2px ${oe(d.palette.common.black,.24)}`}},u+f)),e.length>o&&n.jsx(q,{component:"span",sx:{typography:"subtitle2"},children:`+${r}`})]})}Ve.propTypes={colors:x.arrayOf(x.string),limit:x.number,sx:x.object};function Te({product:e}){const o=n.jsx(jo,{variant:"filled",color:e.status==="sale"&&"error"||"info",sx:{zIndex:9,top:16,right:16,position:"absolute",textTransform:"uppercase"},children:e.status}),t=n.jsx(q,{component:"img",alt:e.name,src:e.cover,sx:{top:0,width:1,height:1,objectFit:"cover",position:"absolute"}}),s=n.jsxs(I,{variant:"subtitle1",children:[n.jsx(I,{component:"span",variant:"body1",sx:{color:"text.disabled",textDecoration:"line-through"},children:e.priceSale&&je(e.priceSale)})," ",je(e.price)]});return n.jsxs(io,{children:[n.jsxs(q,{sx:{pt:"100%",position:"relative"},children:[e.status&&o,t]}),n.jsxs(y,{spacing:2,sx:{p:3},children:[n.jsx(lo,{color:"inherit",underline:"hover",variant:"subtitle2",noWrap:!0,children:e.name}),n.jsxs(y,{direction:"row",alignItems:"center",justifyContent:"space-between",children:[n.jsx(Ve,{colors:e.colors}),s]})]})]})}Te.propTypes={product:x.object};const hn=[{value:"featured",label:"Featured"},{value:"newest",label:"Newest"},{value:"priceDesc",label:"Price: High-Low"},{value:"priceAsc",label:"Price: Low-High"}];function fn(){const[e,o]=h.useState(null),t=r=>{o(r.currentTarget)},s=()=>{o(null)};return n.jsxs(n.Fragment,{children:[n.jsxs(fe,{disableRipple:!0,color:"inherit",onClick:t,endIcon:n.jsx(_,{icon:e?"eva:chevron-up-fill":"eva:chevron-down-fill"}),children:["Sort By: ",n.jsx(I,{component:"span",variant:"subtitle2",sx:{color:"text.secondary"},children:"Newest"})]}),n.jsx(co,{open:!!e,anchorEl:e,onClose:s,anchorOrigin:{vertical:"bottom",horizontal:"right"},transformOrigin:{vertical:"top",horizontal:"right"},slotProps:{paper:{sx:{[`& .${uo.root}`]:{p:0}}}},children:hn.map(r=>n.jsx(po,{selected:r.value==="newest",onClick:s,children:r.label},r.value))})]})}const xn=["Men","Women","Kids"],mn=["All","Shose","Apparel","Accessories"],gn=["up4Star","up3Star","up2Star","up1Star"],vn=[{value:"below",label:"Below $25"},{value:"between",label:"Between $25 - $75"},{value:"above",label:"Above $75"}],bn=["#00AB55","#000000","#FFFFFF","#FFC0CB","#FF4842","#1890FF","#94D82D","#FFC107"];function Be({openFilter:e,onOpenFilter:o,onCloseFilter:t}){const s=n.jsxs(y,{spacing:1,children:[n.jsx(I,{variant:"subtitle2",children:"Gender"}),n.jsx(Ae,{children:xn.map(a=>n.jsx(ee,{control:n.jsx(ho,{}),label:a},a))})]}),r=n.jsxs(y,{spacing:1,children:[n.jsx(I,{variant:"subtitle2",children:"Category"}),n.jsx(pe,{children:mn.map(a=>n.jsx(ee,{value:a,control:n.jsx(de,{}),label:a},a))})]}),u=n.jsxs(y,{spacing:1,children:[n.jsx(I,{variant:"subtitle2",children:"Colors"}),n.jsx(pn,{name:"colors",selected:[],colors:bn,onSelectColor:a=>[].includes(a),sx:{maxWidth:38*4}})]}),f=n.jsxs(y,{spacing:1,children:[n.jsx(I,{variant:"subtitle2",children:"Price"}),n.jsx(pe,{children:vn.map(a=>n.jsx(ee,{value:a.value,control:n.jsx(de,{}),label:a.label},a.value))})]}),d=n.jsxs(y,{spacing:1,children:[n.jsx(I,{variant:"subtitle2",children:"Rating"}),n.jsx(pe,{children:gn.map((a,i)=>n.jsx(ee,{value:a,control:n.jsx(de,{disableRipple:!0,color:"default",icon:n.jsx(ke,{readOnly:!0,value:4-i}),checkedIcon:n.jsx(ke,{readOnly:!0,value:4-i}),sx:{"&:hover":{bgcolor:"transparent"}}}),label:"& Up",sx:{my:.5,borderRadius:1,"&:hover":{opacity:.48}}},a))})]});return n.jsxs(n.Fragment,{children:[n.jsx(fe,{disableRipple:!0,color:"inherit",endIcon:n.jsx(_,{icon:"ic:round-filter-list"}),onClick:o,children:"Filters "}),n.jsxs(fo,{anchor:"right",open:e,onClose:t,PaperProps:{sx:{width:280,border:"none",overflow:"hidden"}},children:[n.jsxs(y,{direction:"row",alignItems:"center",justifyContent:"space-between",sx:{px:1,py:2},children:[n.jsx(I,{variant:"h6",sx:{ml:1},children:"Filters"}),n.jsx(xo,{onClick:t,children:n.jsx(_,{icon:"eva:close-fill"})})]}),n.jsx(mo,{}),n.jsx(go,{children:n.jsxs(y,{spacing:3,sx:{p:3},children:[s,r,u,f,d]})}),n.jsx(q,{sx:{p:3},children:n.jsx(fe,{fullWidth:!0,size:"large",type:"submit",color:"inherit",variant:"outlined",startIcon:n.jsx(_,{icon:"ic:round-clear-all"}),children:"Clear All"})})]})]})}Be.propTypes={openFilter:x.bool,onOpenFilter:x.func,onCloseFilter:x.func};const yn=N("div")(({theme:e})=>({zIndex:999,right:0,display:"flex",cursor:"pointer",position:"fixed",alignItems:"center",top:e.spacing(16),height:e.spacing(5),paddingLeft:e.spacing(2),paddingRight:e.spacing(2),paddingTop:e.spacing(1.25),boxShadow:e.customShadows.z20,color:e.palette.text.primary,backgroundColor:e.palette.background.paper,borderTopLeftRadius:Number(e.shape.borderRadius)*2,borderBottomLeftRadius:Number(e.shape.borderRadius)*2,transition:e.transitions.create("opacity"),"&:hover":{opacity:.72}}));function Cn(){return n.jsx(yn,{children:n.jsx(vo,{showZero:!0,badgeContent:0,color:"error",max:99,children:n.jsx(_,{icon:"eva:shopping-cart-fill",width:24,height:24})})})}function jn(){const[e,o]=h.useState(!1),t=()=>{o(!0)},s=()=>{o(!1)};return n.jsxs(bo,{children:[n.jsx(I,{variant:"h4",sx:{mb:5},children:"Products"}),n.jsx(y,{direction:"row",alignItems:"center",flexWrap:"wrap-reverse",justifyContent:"flex-end",sx:{mb:5},children:n.jsxs(y,{direction:"row",spacing:1,flexShrink:0,sx:{my:1},children:[n.jsx(Be,{openFilter:e,onOpenFilter:t,onCloseFilter:s}),n.jsx(fn,{})]})}),n.jsx(Ce,{container:!0,spacing:3,children:dn.map(r=>n.jsx(Ce,{xs:12,sm:6,md:3,children:n.jsx(Te,{product:r})},r.id))}),n.jsx(Cn,{})]})}function kn(){return n.jsxs(n.Fragment,{children:[n.jsx(yo,{children:n.jsx("title",{children:" Products | Minimal UI "})}),n.jsx(jn,{})]})}export{kn as default};
