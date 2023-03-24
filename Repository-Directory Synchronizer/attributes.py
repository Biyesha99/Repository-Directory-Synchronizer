import os, filecmp, shutil


class Dircmp:


    def __init__(self, d1, d2):
        self.d1 = os.path.join(d1, '')
        self.d2 = os.path.join(d2, '')



    ## methods for comparison
    def dc(self, d):
        '''returns a list containing all the files of the given directory d'''
        
        allFiles = []
        allDirs = []
        for root, subdirs, files in os.walk(d):
            for file in files:
                allFiles.append(os.path.join(root, file).split(d)[1])

            for subdir in subdirs:
                allDirs.append(os.path.join(root, subdir).split(d)[1])
                
        
        return allFiles, allDirs



    
    def onlys(self, list1, list2):
        '''returns a list containing the files that are in list1 but not in list2'''
        only_in_list1 = []
        for item in list1:
            if item not in list2:
                only_in_list1.append(item)

        return only_in_list1
    
    

    def commons(self, list1, list2):
        '''returns list1 <intersection> list2'''

        comm_items = []
        for item in list1[:]:
            if item in list2[:]:
                comm_items.append(item)

        return comm_items
    
    

    def common_but(self):
        '''name same, but content or metadata not same'''

        files = []
        join = os.path.join
        for file in self.comm_files[:]:
            if not filecmp.cmp(join(self.d1, file), join(self.d2, file), shallow = False):
                files.append( ( join ( self.d1, file ), join ( self.d2, file ) ) )
        self.funnies = files[:]
        return files
    


    def funnies_statAndReport(self):
        import time
        stats = {}
        report = ""
        for file1, file2 in self.funnies:
            fn = file1.split(self.d1)[1]
            stat1 = os.stat(file1)
            stat2 = os.stat(file2)

            size_cmp = ''
            lmd_cmp = ''
            if stat1.st_size > stat2.st_size:
                size_cmp = 'Larger'
            elif stat1.st_size < stat2.st_size:
                size_cmp = 'Smaler'
            else:
                size_cmp = 'Same size'

            if stat1.st_mtime > stat2.st_mtime:
                lmd_cmp = 'Newer'
            elif stat1.st_mtime < stat2.st_mtime:
                lmd_cmp = 'Older'
            else:
                lmd_cmp = 'Same time'

            temp = {
                    self.d1 : {'size': stat1.st_size, 'last mod': stat1.st_mtime, 'stat obj': stat1},
                    self.d2 : {'size': stat2.st_size, 'last mod': stat2.st_mtime, 'stat obj': stat2}
                    }

            report += "File {0}:\n\tFrom {1}: ({4}) ({5})\n\t\tSize: {2} MB\n\t\tLast modified on {3}".format(
                fn, self.d1, stat1.st_size/(1024)**2, time.strftime('%c, GMT%z', time.localtime(stat1.st_mtime)), size_cmp, lmd_cmp
                )

            report += "\n\tFrom {0}:\n\t\tSize: {1} MB\n\t\tLast modified on {2}\n\n\n".format(
                self.d2, stat2.st_size/(1024)**2, time.strftime('%c, GMT%z', time.localtime(stat2.st_mtime))
                )
            
            stats[fn] = temp

        self.funnies_report = report
        self.funnies_stats = stats
        print(report)
        return stats


    ## methods for syncing
    def mkdir(self, subdirs, dest, avoid = None):
        '''create all the subdirs in dest'''
        for subdir in subdirs[:]:
            if avoid:
                if subdir in avoid:
                    continue

            print("[*] Creating directory <%s> in <%s>"%(subdir, dest))
            os.mkdir(os.path.join(dest, subdir))


    
    def _sync(self, src, files, dirs, trg, avoid_files = None, avoid_dirs = None):
        '''
        Creates directories and files in *trg* directory
        
        object._sync(src, files, dirs, trg, avoid_files = None, avoid_dirs = None)
        
        Arguments:
            :src:  name of the root directory whose files and subdirectories are to be copied --> string
            :files:  names of the files which are to be copied --> list
            :dirs:  names of the subdirectories which are to be copied --> list
            :avoid_files:  (optional) names of the files which are to be skipped while copying --> list
            :avoid_dirs:  (optional) names of the subdirectories which are to be skipped while copying --> list
        Returns nothing
        '''
        
        join = os.path.join

        self.mkdir(dirs[:], trg, avoid_dirs)
        
        for file in files[:]:
            if avoid_files:
                if file in avoid_files:
                    continue
            dn = os.path.split(file)[0]
            if avoid_dirs:
                if dn in avoid_dirs:
                    continue

            print("[*] Creating file <%s> in <%s>"%(file, join(trg, dn)))
            shutil.copy2(join(src, file), join(trg, dn))
        
        

    def sync_left(self, avoid_files = None, avoid_dirs = None):
        """
        Copies the only_rights to d1
        """
        self._sync(self.d2, self.only_right_files[:], self.only_right_dirs[:], self.d1, avoid_files, avoid_dirs)
        print('[*] Synced %s with %s'%(self.d1, self.d2))
        


    def sync_right(self, avoid_files = None, avoid_dirs = None):
        """
        Copies the only_left to d2
        """
        self._sync(self.d1, self.only_left_files[:], self.only_left_dirs[:], self.d2, avoid_files, avoid_dirs)
        print('[*] Synced %s with %s'%(self.d2, self.d1))


    def sync(self, avoid_files = None, avoid_dirs = None):
        self.sync_left(avoid_files, avoid_dirs)
        self.sync_right(avoid_files, avoid_dirs)


## Creating Instance Attributes
def methodOne(self1):
    self.left_files, self.left_dirs = self.dc(self.d1)

def methodTwo(self):
    self.right_files, self.right_dirs = self.dc(self.d2)

def methodThree(self):
    self.only_left_files = self.onlys(self.left_files,self.right_files)

def methodFour(self):
    self.only_left_dirs = self.onlys(self.lef_dirs,self.right_dirs)

def methodFive(self):
    self.only_right_files = self.onlys(self.right_files,self.left_files)

def methodSix(self):
    self.only_right_dirs = self.onlys(self.right_dirs,self.lef_dirs)

def methodSeven(self):
    self.comm_files = self.commons(self.left_files,self.right_files)

def methodEight(self):
    self.comm_dirs = self.commons(self.left_dirs, self.right_dirs)


methodmap = dict(
    left_files = methodOne, left_dirs = methodOne,
    right_files = methodTwo, right_dirs = methodTwo,
    only_left_files = methodThree, only_right_files = methodFive, only_left_dirs = methodFour, only_right_dirs = methodSix,
    comm_files = methodSeven, comm_dirs = methodEight,
    funnies = common_but,
    funnies_stats = funnies_statAndReport, funnies_report = funnies_statAndReport
)

def __getattr__(self, attr):
    if sttr not in self.methodmap:
        raise AttributeError(attr)

    self.methodmap[attr](self)
    return getattr(self, attr)

    