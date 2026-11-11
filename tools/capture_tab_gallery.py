#!/usr/bin/env python3
"""Capture every accessible Designer tab in its full-window context.

Uses an empty GUI, isolated settings, and no network. Never fabricates data.
Pass --qso to audit the actual -QSO launch and capture its shared GP page.
"""
import os, sys, json, hashlib, traceback, shutil
from pathlib import Path
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
MANUAL = ROOT/'exostriker-manual'
CACHE = Path('/tmp/exostriker-manual-capture')
CACHE.mkdir(exist_ok=True)
QSO = '--qso' in sys.argv
UNNAMED_ONLY = '--only-unnamed' in sys.argv
sys.argv = [sys.argv[0]] + (['-QSO'] if QSO else [])
sys.path[:0] = [str(ROOT), str(ROOT/'exostriker/lib')]
os.environ.update(QT_QPA_PLATFORM='offscreen', EXOSTRIKER_PREWARM_INIT='0',
    MPLCONFIGDIR=str(CACHE/'mpl'), NUMBA_CACHE_DIR=str(CACHE/'numba'),
    IPYTHONDIR=str(CACHE/'ipython'), JUPYTER_RUNTIME_DIR=str(CACHE/'jupyter'))
log = open(CACHE/('qso-gallery.log' if QSO else 'tab-gallery.log'), 'w', buffering=1)
code = 0
try:
    import application_paths
    settings = CACHE/('qso-gallery-settings.json' if QSO else 'tab-gallery-settings.json')
    shutil.copyfile(ROOT/'exostriker/lib/ES_settings.json',settings)
    application_paths.user_settings_path = lambda: str(settings)
    import exostriker.gui as g
    from PyQt6 import QtWidgets, QtCore, QtGui
    from unittest.mock import patch
    os.chdir(CACHE)
    g._application.setStyle('Fusion')
    with patch('RVBank_window.urlopen',side_effect=OSError('Offline capture')), patch.object(g.UpdateCheck,'start'):
        w = g.Exo_striker()
    # Fail clearly if an unexpected dialog would otherwise block an unattended capture.
    def unexpected(*args,**kwargs):
        raise RuntimeError('Unexpected capture dialog: '+str(args[1:]))
    QtWidgets.QMessageBox.critical = unexpected
    QtWidgets.QMessageBox.warning = unexpected
    w.save_last_session = lambda *args,**kwargs: None
    # Documentation placeholders must contain no fabricated or imported data.
    # The normal constructor already supplies an empty session.
    assert not any(len(row) for row in g.fit.rv_data_sets.values())
    assert not any(len(row) for row in g.fit.act_data_sets.values())
    demo = g.fit
    w.resize(1600,1240)
    w.param_tabs.setMaximumHeight(480)
    w.param_tabs.setMinimumHeight(450)
    w.gridLayout_122.setRowMinimumHeight(4,490)
    w.show()
    out=MANUAL/'docs/source/images/current/tabs';out.mkdir(exist_ok=True)
    def events():
        for _ in range(3):g._application.processEvents()
    def reveal(widget):
        parent=widget.parentWidget()
        while parent is not None:
            if isinstance(parent,QtWidgets.QTabWidget):
                for i in range(parent.count()):
                    page=parent.widget(i)
                    if page is widget or page.isAncestorOf(widget):
                        parent.setCurrentWidget(page);break
            parent=parent.parentWidget()
    def path_for(widget):
        parts=[];parent=widget.parentWidget()
        while parent is not None:
            if isinstance(parent,QtWidgets.QTabWidget):
                for i in range(parent.count()):
                    page=parent.widget(i)
                    if page is widget or page.isAncestorOf(widget):
                        parts.append(parent.tabText(i).replace('&',''));break
            parent=parent.parentWidget()
        return list(reversed(parts))
    def reset():
        reveal(w.tab_timeseries_RV);reveal(w.tab_RV_pl_param)
        reveal(w.RV_time_series_tab);w.tabWidget_8.setCurrentIndex(0)
        reveal(w.tab_185);reveal(w.tab_144)
    def purpose(path):
        text=' / '.join(path).lower()
        rules=[
            ('magnetic cycle','Enable the sine separately from GP; choose an activity file, Fit flags, phase offset, bounds and priors. READ ME explains the shared period.'),
            ('joint act.','Include each loaded indicator separately. Activity responses, offsets and jitter have their own Fit flags, bounds and priors; READ ME explains units and cost.'),
            ('correlations','Choose two series. Cross hair inspects coordinates; Go to plot options opens correlation labels, color, errors and regression display.'),
            ('activity / gls','Select an indicator; o-c switches to model residuals, or mean-subtracted data without a model. Print info reports the current periodogram.'),
            ('activity / time','Choose an indicator; o-c shows model/mean residuals. Cross hair and Legend are optional; Go to plot options opens styling.'),
            ('plot opt. / activity','Size, Alpha, Symbol and Color follow RV/transit controls. Model styling and correlation label/color/error controls share this page.'),
            ('fortran','Choose LM/Simplex stages and run counts. LM and Simplex pages expose convergence limits, tolerances and step controls; settings live in the session.'),
            ('scipy','Choose the Python optimizers and their run counts. GP, cycle and astrometry models use the Python likelihood path where required.'),
            ('mcmc','Choose walkers, steps and starting points, then Run MCMC. Check priors and inspect posterior diagnostics; a screenshot does not establish convergence.'),
            ('nest.','Choose live points, stopping rules and result summaries, then Run Nest.samp. Inspect diagnostics before interpreting evidence.'),
            ('hipparcos','Import Hipparcos and/or Gaia data and select their independent Fit checkboxes. Unchecked missions do not contribute to the likelihood.'),
            ('dilution','Set the contamination/dilution treatment per photometric dataset. Enable only parameters supported by your data.'),
            ('limb','Choose the limb-darkening law and coefficients for each transit dataset, with physically meaningful bounds and priors.'),
            ('limits','Set hard bounds and one prior family per coordinate. Gaussian priors need positive sigma; Jeffreys limits must be positive and ordered.'),
            ('kernel','Review the kernel parameters and units; Fit flags choose free coordinates. GP priors are configured under Limits and Priors.'),
            ('gp param.','Enable the RV or transit GP separately; select a kernel, its parameters and Fit flags. The activity shortcut opens the joint RV/activity page.'),
            ('stellar','Stellar inputs set physical scales. Density-mode transit geometry uses stellar-density bounds and priors rather than a/R-star bounds.'),
            ('parameterisation','Choose orbital/transit coordinates consistently. In density mode, the density replaces a/R-star as the fitted coordinate.'),
            ('n-body','Configure integration duration, step, accuracy and output. Viewing this page does not run an orbital integration.'),
            ('gls','Set period/frequency search ranges and resolution. Interpret peaks with the sampling window and residual model in mind.'),
            ('planet param.','Include a planet and choose free parameters before Initialize/Fit. Values, units and uncertainty labels share the same row.'),
            ('data options','Open dataset processing tools or configure per-dataset options. Save a session before changing the data.'),
            ('offset','Each loaded dataset has its own offset and jitter. Check Fit to vary a nuisance parameter; use meaningful bounds.'),
            ('trends','Configure dataset baseline trends and fit flags. Check degeneracy with long-period signals.'),
            ('axes','Select the target plot and adjust labels, ranges and appearance; Apply updates the target view.'),
            ('cornerplot','Choose posterior coordinates and appearance after samples exist. No sampler has been run for this capture.'),
        ]
        return next((description for key,description in rules if key in text),
            'Open the named tab to configure or inspect this part of the analysis. Initialize evaluates the model; Fit and sampling are separate actions.')
    manifest=[]
    def annotate(filename,title,description,dialog=None,target=None):
        events();original=w.grab();width,height=original.width(),original.height()
        pix=QtGui.QPixmap(width,height+230);pix.fill(QtGui.QColor('#f2f5f9'))
        painter=QtGui.QPainter(pix);painter.drawPixmap(0,0,original)
        if dialog is not None:
            # Real Qt dialog grab, composited over the real window for headless capture.
            painter.drawPixmap(width-dialog.width()-30,80,dialog.grab())
        regions=[w.menuBar(),w.plot_tabs,w.comboBox_select_ses,w.param_tabs,w.tabWidget_helper,w.tabWidget_data_section]
        for n,region in enumerate(regions,1):
            point=region.mapTo(w,QtCore.QPoint(region.width()-14,14))
            if n==1:point=QtCore.QPoint(230,10)
            painter.setPen(QtGui.QPen(QtGui.QColor('white'),2));painter.setBrush(QtGui.QColor('#163e73'))
            painter.drawEllipse(point,12,12);painter.setFont(QtGui.QFont('DejaVu Sans',10,QtGui.QFont.Weight.Bold))
            painter.drawText(QtCore.QRect(point.x()-12,point.y()-12,24,24),QtCore.Qt.AlignmentFlag.AlignCenter,str(n))
        notes=['Menus: save sessions, edit display names, export results and open help.',
            'PLACEHOLDER: empty GUI, no observations or fitted models. The author will supply real examples.',
            'Session controls: Initialize evaluates; Fit / Run MCMC / Run Nest.samp. infer parameters; Stop cancels a supervised calculation.',
            description,
            'Accessory tools remain in context. No fit, sampler, period search or orbital integration was run for this placeholder.',
            'Dataset imports, use flags, nuisance parameters and dataset priors stay accessible beside the selected tab.']
        if target is not None:
            region=1 if w.plot_tabs.isAncestorOf(target) else 5 if w.tabWidget_data_section.isAncestorOf(target) else 4 if w.tabWidget_helper.isAncestorOf(target) else 3
            if region!=3:
                notes[3]='Parameter and plot-option tabs remain accessible below the scientific plots.'
                notes[region]=description
        if dialog is not None:
            notes[3]='Parameter and plot-option tabs remain accessible below the scientific plots.'
            notes[4]=description
        painter.setPen(QtGui.QColor('#163e73'));painter.setFont(QtGui.QFont('DejaVu Sans',12,QtGui.QFont.Weight.Bold))
        painter.drawText(18,height+25,'PLACEHOLDER — '+title)
        for i,note in enumerate(notes):
            painter.setFont(QtGui.QFont('DejaVu Sans',10))
            painter.drawText(QtCore.QRect(18+(i%2)*(width//2),height+40+(i//2)*60,width//2-35,57),QtCore.Qt.TextFlag.TextWordWrap,str(i+1)+'. '+note)
        painter.end();assert pix.save(str(out/filename))
        record=dict(file='tabs/'+filename,title=title,description=description,callouts=notes)
        manifest.append(record);return record
    if QSO:
        reveal(w.tab_60)
        forbidden=[w.tab_79,w.tab_activity_joint_gp,w.tab_magnetic_cycle]
        assert all(not w.tabWidget_14.isTabVisible(w.tabWidget_14.indexOf(page)) for page in forbidden)
        assert w.activity_gp_open.isHidden()
        for name in ('act_model_width','act_model_width_caption','act_pushButton_color_21','act_pushButton_color_21_caption'):
            assert getattr(w,name).isHidden()
        assert w.QSO_str=='QSO'
        record=annotate('qso-mode.png','QSO mode — shared GP and sine workflow',
            'The -QSO launch retains its GP page. Transit/joint activity/magnetic-cycle pages and stellar-activity selector/model controls are hidden.')
        record['group']='QSO mode'
        record['visible_gp_tabs']=[w.tabWidget_14.tabText(i) for i in range(w.tabWidget_14.count()) if w.tabWidget_14.isTabVisible(i)]
    else:
        # Capture each accessible tab defined in the maintained Designer source.
        ui=ET.parse(ROOT/'exostriker/lib/UI/es.ui').getroot()
        for node in ui.iter('widget'):
            if node.get('class')!='QTabWidget':continue
            tabs=getattr(w,node.get('name'),None)
            if not isinstance(tabs,QtWidgets.QTabWidget):continue
            for i in range(tabs.count()):
                if not tabs.isTabVisible(i):continue
                page=tabs.widget(i)
                if UNNAMED_ONLY and page.objectName():continue
                reset();reveal(page)
                if not page.isVisibleTo(w):continue
                path=path_for(page);title=' → '.join(path)
                page_key=page.objectName() or tabs.objectName()+'-'+str(i)
                item=annotate(page_key+'.png',title,purpose(path),target=page)
                if w.plot_tabs.isAncestorOf(page):group='Scientific plots'
                elif w.tabWidget_data_section.isAncestorOf(page):group='Datasets'
                elif w.tabWidget_helper.isAncestorOf(page):group='Accessories'
                elif w.param_tabs.isAncestorOf(page):
                    group={'GP param.':'Gaussian processes','Limits and Priors':'Bounds and priors',
                           'Model opt.':'Model and inference','N-body':'Model and inference',
                           'Plot opt.':'Plot appearance'}.get(path[0],'Physical parameters')
                else:group='Accessories'
                item.update(group=group,path=path,widget=page_key,tab_widget=tabs.objectName())
                log.write(title+'\n')
        # Add explicit illustrations of new combinations, beyond the individual tabs.
        for name,page,residual in [('activity-residuals',w.Activity_index_timeseries_plot,True),('activity-residual-gls',w.activity_index_periodograms,True),('activity-correlation-options',w.Correlations_timeseries_plot,False)]:
            reset();reveal(page);reveal(w.tab_21);reveal(w.tab_24)
            w.act_plot_o_c.setChecked(residual);w.gls_act_o_c.setChecked(residual)
            w.act_plot_cross_hair.setChecked(True);w.act_plot_legend.setChecked(True)
            w.comboBox_act_data.setCurrentIndex(0);w.comboBox_act_data_gls.setCurrentIndex(0)
            if page is w.Correlations_timeseries_plot:
                w.corr_plot_cross_hair.setChecked(True)
            item=annotate(name+'.png',name.replace('-',' ').title(),purpose(path_for(page)),target=page)
            item['group']='New activity workflows'
        reset();reveal(w.Activity_index_timeseries_plot);reveal(w.tab_21)
        dialog=g.DatasetNamesDialog(demo,w);dialog.show();events()
        item=annotate('dataset-names.png','Edit file names — activity datasets included',
            'Edit display names for loaded datasets, including Activity. Apply updates selectors, legends and GP/cycle labels; Cancel leaves names unchanged.',dialog)
        item['group']='New activity workflows';dialog.reject()
    sources=['gui.py','lib/UI/es.ui','lib/es.py','lib/qso.py','lib/activity_gp.py','lib/magnetic_cycle.py','lib/dataset_names_window.py']
    if UNNAMED_ONLY:
        previous=json.loads((out.parent/'tab-gallery-manifest.json').read_text())['screenshots']
        merged={item['file']:item for item in previous if item.get('widget','present')}
        merged.update({item['file']:item for item in manifest})
        manifest=list(merged.values())
    metadata=dict(placeholder=True,version=g.__version__,captured_utc=datetime.now(timezone.utc).isoformat(),
        qt=QtCore.QT_VERSION_STR,platform='offscreen',style='Fusion',qso=QSO,
        data='Empty GUI placeholder. No observations, synthetic data, fitted models or private sessions.',
        source_sha256={name:hashlib.sha256((ROOT/'exostriker'/name).read_bytes()).hexdigest() for name in sources},screenshots=manifest)
    (out.parent/('qso-provenance.json' if QSO else 'tab-gallery-manifest.json')).write_text(json.dumps(metadata,indent=2))
    log.write('PASS: '+str(len(manifest))+' full-window captures\n')
except BaseException:
    code=1;traceback.print_exc(file=log)
finally:
    log.close();os._exit(code)
