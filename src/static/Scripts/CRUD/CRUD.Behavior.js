; (function(jQuery)
{
    jQuery.extend(jQuery.CRUD,
	{
	    Behavior: function(Options)
	    {
	        var CRUD = this;

	        var Operations =
            {
                Query: "query",
                Insert: "insert",
                Update: "update",
                Delete: "delete"
            };

            function Save(Callback)
            {
                if(B.Operation == Operations.Insert || B.Operation == Operations.Update)
			    {
			        B.Core.View.ShowWait();
			        var Record = CRUD.View.Form.Get(B.Operation == Operations.Update);

                    var State = true;
                    if(B.BeforeSave)
			        {
			            State = B.BeforeSave(Record, function(State)
                        {
                            if(State)
                            {
			                    CRUD.View.Form.Validate(Record, function(State)
			                    {
			                        if(State)
			                        {
			                            if(B.Operation == Operations.Insert)
			                            {
			                                CRUD.Service.Insert(Record, Callback);
			                            }
			                            else
			                            {
			                                CRUD.Service.Update(Record, Callback);
			                            }
			                        }
			                        else
			                        {
			                            B.Core.View.CloseWait();
			                        }
			                    });
                            }
                            else
                            {
                                B.Core.View.CloseWait();
                            }
                        });
			        }

                    if(State)
                    {
			            CRUD.View.Form.Validate(Record, function(State)
			            {
			                if(State)
			                {
			                    if(B.Operation == Operations.Insert)
			                    {
			                        CRUD.Service.Insert(Record, Callback);
			                    }
			                    else
			                    {
			                        CRUD.Service.Update(Record, Callback);
			                    }
			                }
			                else
			                {
			                    B.Core.View.CloseWait();
			                }
			            });
                    }
                    else
                    {
                        B.Core.View.CloseWait();
                    }
			    }
            };

	        function Save_CB(Result)
	        {
	            if(Result.Code == 0)
	            {
	                var State = true;

	                if(B.AfterSave)
	                {
	                    State = B.AfterSave(Result);
	                }
	                CRUD.View.CloseWait();
	                if(State)
	                {
	                    if(B.Operation == Operations.Insert)
	                    {
	                        //CRUD.View.Grid.Refresh();
                            if(jQuery.isArray(Result.Response))
                            {
                                for(var i = 0, Arr = Result.Response, len = Arr.length; i < len; i++)
                                {
                                    CRUD.View.Grid.InsertRow(Arr[i], 0);
                                }
                            }
                            else
                            {
                                CRUD.View.Grid.InsertRow(Result.Response, 0);
                            }

                            if(CRUD.View.Object.Layout != "POP")
                            {
	                            CRUD.View.Form.Clear();
                            }
                            if(Options.AutoInsert == true)
                            {
                                setTimeout(function(){CRUD.View.Button.Click("insert");}, 90);
                            }
                            else
                            {
                                CRUD.View.ShowDialog({ Title: "提示", Type: window.top.MyDialog.Types.Message, Icon: window.top.MyDialog.Icons.Info, Message: "保存成功", AutoClose: 5});
                            }
	                    }
	                    else
	                    {
	                        CRUD.View.Grid.UpdateRow(Result.Response);
	                        CRUD.View.Button.Normal(["update", "delete"]);
                            CRUD.View.ShowDialog({ Title: "提示", Type: window.top.MyDialog.Types.Message, Icon: window.top.MyDialog.Icons.Info, Message: "保存成功", AutoClose: 5});
	                    }
	                    B.Operation = Operations.Query;
                        if(CRUD.View.Object.Layout != "POP")
                        {
	                        CRUD.View.Form.Disable();
                        }
                        else
                        {
                            //CRUD.View.Dialog.Close();//对话框关闭逻辑有问题
                        }
	                    CRUD.View.Button.Disable(["confirm", "cancel"]);
	                    CRUD.View.Button.Enable(["insert", "upsert"]);
	                    CRUD.View.Button.Normal(["insert", "upsert"]);
                        if(CRUD.View.Form.Auto)
                        {
                            CRUD.View.Form.Resize(CRUD.View.Form.Auto.Query);
                        }
	                }
	            }
	            else
	            {
	                CRUD.View.CloseWait();
	                //显示失败提示
	                CRUD.View.ShowMessage(Result.Message);
	            }
	        };

	        function Delete_CB(Result)
	        {
	            if(Result.Code == 0)
	            {
	                var State = true;

	                if(B.AfterDelete)
	                {
	                    State = B.AfterDelete(Result);
	                }
	                CRUD.View.CloseWait();
	                if(State)
	                {
                        CRUD.View.ShowDialog({ Title: "提示", Type: window.top.MyDialog.Types.Message, Icon: window.top.MyDialog.Icons.Info, Message: "删除成功", AutoClose: 5});
	                    B.Operation = Operations.Query;
	                    CRUD.View.Grid.Refresh();
                        if(CRUD.View.Object.Layout != "POP")
                        {
	                        CRUD.View.Form.Clear();
	                        CRUD.View.Form.Disable();
                        }
	                    CRUD.View.Button.Disable(["update", "delete", "confirm", "cancel"]);
	                    CRUD.View.Button.Enable(["insert", "upsert"]);
	                }
	            }
	            else
	            {
	                CRUD.View.CloseWait();
	                CRUD.View.ShowMessage(Result.Message);
	            }
	        };

	        var B =
			{
			    Core: CRUD,
			    Operation: Operations.Query,
			    ButtonClick: function()
			    {
			        var Command = jQuery(this).attr("command");
			        if(CRUD.View.Button.Enabled(Command))
			        {
                        if(B.Button.BeforeClick)
                        {
                            B.Button.BeforeClick(Command);
                        }
			            switch(Command)
			            {
			                case "reset":
			                    {
			                        CRUD.View.Reset();
                                    if(CRUD.View.Object.Quicks && CRUD.View.Object.Quicks.length > 0)
                                    {
                                        CRUD.View.Button.Click("query");
                                    }
                                    else
                                    {
			                            CRUD.View.Grid.Refresh();
                                    }
			                        CRUD.View.Button.Normal(["filter", "order", "column"]);
			                    }
			                    break;
			                case "filter":
			                    {
			                        CRUD.View.ShowFilter({}, function(Result)
			                        {
			                            if(Result.length > 0)
			                            {
			                                CRUD.View.Button.Highlight("filter");
			                            }
			                            else
			                            {
			                                CRUD.View.Button.Normal("filter");
			                            }

                                        //
//                                        var State = false;
//                                        for(var Key in CRUD.View.Column)
//                                        {
//                                            if(CRUD.View.Column[Key].hidden == true)
//                                            {
//                                                State = true;
//                                                break;
//                                            }
//                                        }
//                                        if(State)
//			                            {
//			                                CRUD.View.Button.Highlight("order");
//			                            }
//			                            else
//			                            {
//			                                CRUD.View.Button.Normal("order");
//			                            }

			                            CRUD.View.Grid.Refresh();
			                        });
			                    }
			                    break;
			                case "order":
			                    {
			                        CRUD.View.ShowOrder({}, function(Result)
			                        {
//			                            if(Result.length > 0)
//			                            {
//			                                CRUD.View.Button.Highlight("order");
//			                            }
//			                            else
//			                            {
//			                                CRUD.View.Button.Normal("order");
//			                            }
			                            CRUD.View.Grid.Refresh();
			                        });
			                    }
			                    break;
			                case "column":
			                    {
			                        CRUD.View.ShowColumn({}, function(Result)
			                        {
			                            if(Result)
			                            {
			                                CRUD.View.Button.Highlight("column");
			                            }
			                            else
			                            {
			                                CRUD.View.Button.Normal("column");
			                            }
			                        });
			                    }
			                    break;
			                case "query":
			                    {
			                        CRUD.View.QuickFilter({}, function(Filters)
			                        {
			                            CRUD.View.Grid.Refresh();
			                            if(Filters.length > 0)
			                            {
			                                CRUD.View.Button.Highlight("filter");
			                            }
			                            else
			                            {
			                                CRUD.View.Button.Normal("filter");
			                            }
			                        });
			                    }
			                    break;
			                case "insert":
                            case "upsert":
			                    {
                                    B.Operation = Operations.Insert;
                                    if(CRUD.View.Object.Layout == "POP")
                                    {

                                        ShowDialog({ Title: "增加", Width: 800, Height:600, Content: CRUD.View.DialogForm }, {Command:"insert",Save:Save, Success:Save_CB});
                                    }
                                    else
                                    {
			                            CRUD.View.Form.Disable();
                                        CRUD.View.Form.Enable();
                                        if(Command == "insert")
                                        {
			                                CRUD.View.Form.Clear();
                                        }
                                        CRUD.View.Form.Set(Command);
			                            CRUD.View.Button.Enable(["confirm", "cancel"]);
			                            CRUD.View.Button.Normal(["insert", "upsert", "update"]);
			                            CRUD.View.Button.Highlight(Command);
                                        if(CRUD.View.Form.Auto)
                                        {
                                            CRUD.View.Form.Resize(CRUD.View.Form.Auto.Edit);
                                        }
                                    }
                                    B.Operation = Operations.Insert;
			                    }
			                    break;
			                case "update":
			                    {
                                    B.Operation = Operations.Update;
                                    if(CRUD.View.Object.Layout == "POP")
                                    {
                                        ShowDialog({ Title:"编辑", Width: 800, Height:600, Content: CRUD.View.DialogForm }, {Command:"update",Save:Save, Success:Save_CB});
                                    }
                                    else
                                    {
			                            //B.Grid.RowClick(CRUD.View.Grid.CurrentRow, CRUD.View.Grid.CurrentIndex);
                                        if(CRUD.View.Object.Layout != "POP")
                                        {
                                            CRUD.View.Form.Enable();
				                            CRUD.View.Form.Set();
                                        }
			                            CRUD.View.Button.Normal(["insert", "upsert"]);
			                            CRUD.View.Button.Highlight("update");
			                            CRUD.View.Button.Enable(["confirm", "cancel"]);
                                        if(CRUD.View.Form.Auto)
                                        {
                                            CRUD.View.Form.Resize(CRUD.View.Form.Auto.Edit);
                                        }
                                    }
                                    B.Operation = Operations.Update;
			                    }
			                    break;
			                case "delete":
			                    {
			                        var State = true;
			                        if(B.BeforeDelete)
			                        {
			                            State = B.BeforeDelete(CRUD.View.Grid.CurrentRow, function(Result)
                                        {
                                            if(Result)
			                                {
			                                    B.Core.View.ShowWait();
			                                    B.Operation = Operations.Delete;
			                                    CRUD.Service.Delete(CRUD.View.Grid.CurrentRow, Delete_CB);
			                                }
                                        });
			                        }
			                        if(State)
			                        {
			                            CRUD.View.ShowConfirm("确定要删除选中的记录吗？", function(Result)
			                            {
			                                if(Result)
			                                {
			                                    B.Core.View.ShowWait();
			                                    B.Operation = Operations.Delete;
			                                    CRUD.Service.Delete(CRUD.View.Grid.CurrentRow, Delete_CB);
			                                }
			                            });
			                        }
			                    }
			                    break;
			                case "confirm":
			                    {
			                        Save(Save_CB);
			                    }
			                    break;
			                case "cancel":
			                    {
			                        B.Operation = Operations.Query;
			                        CRUD.View.Button.Disable(["confirm", "cancel"]);
			                        CRUD.View.Button.Enable(["insert","upsert"]);
			                        CRUD.View.Button.Normal(["insert","upsert"]);
			                        if(CRUD.View.Grid.CurrentRow)
			                        {
			                            CRUD.View.Button.Normal(["update", "delete"]);
			                        }
			                        else
			                        {
			                            CRUD.View.Button.Disable(["update", "delete"]);
			                            CRUD.View.Form.Clear();
			                        }
                                    CRUD.View.Form.Disable();
                                    if(CRUD.View.Form.Auto)
                                    {
                                        CRUD.View.Form.Resize(CRUD.View.Form.Auto.Query);
                                    }
			                    }
			                    break;
			                case "export":
			                    {
			                        CRUD.View.Grid.Export();
			                    }
			                    break;
			            }
			        }
			    },
                Button:{},
			    Grid:
				{
				    RowClick: function(Row, Index)
				    {
				        if(B.Grid.BeforeRowClick)
				        {
				            B.Grid.BeforeRowClick(Row, Index);
				        }

                        if(CRUD.View.Object.Form || CRUD.View.Object.FormContent)
                        {
                            if(CRUD.View.Object.Layout != "POP")
                            {
                                B.Operation = Operations.Query;
                                CRUD.View.Form.Enable();
				                CRUD.View.Form.Set();
				                CRUD.View.Form.Disable();
                            }
                            CRUD.View.Button.Normal(["insert", "upsert", "update", "delete"]);
				            CRUD.View.Button.Disable(["confirm", "cancel"]);
				            CRUD.View.Button.Enable(["update", "delete"]);
                        }

				        if(B.Grid.AfterRowClick)
				        {
				            B.Grid.AfterRowClick(Row, Index);
				        }
				    },
				    RowDblClick: function(Row)
				    {
                        if(CRUD.View.Object.Form || CRUD.View.Object.FormContent)
                        {
                            CRUD.View.Button.Click("update");
                        }
				    }
				}
			}

	        //query
	        if(jQuery.isFunction(Options.BeforeQuery))
	        {
	            B.BeforeQuery = Options.BeforeQuery;
	        }
	        if(jQuery.isFunction(Options.AfterQuery))
	        {
	            B.AfterQuery = Options.AfterQuery;
	        }

	        //save
	        if(jQuery.isFunction(Options.BeforeSave))
	        {
	            B.BeforeSave = Options.BeforeSave;
	        }
	        if(jQuery.isFunction(Options.AfterSave))
	        {
	            B.AfterSave = Options.AfterSave;
	        }

	        //delete
	        if(jQuery.isFunction(Options.BeforeDelete))
	        {
	            B.BeforeDelete = Options.BeforeDelete;
	        }
	        if(jQuery.isFunction(Options.AfterDelete))
	        {
	            B.AfterDelete = Options.AfterDelete;
	        }

	        //Grid RowClick
	        if(Options.Grid && jQuery.isFunction(Options.Grid.BeforeRowClick))
	        {
	            B.Grid.BeforeRowClick = Options.Grid.BeforeRowClick;
	        }
	        if(Options.Grid && jQuery.isFunction(Options.Grid.AfterRowClick))
	        {
	            B.Grid.AfterRowClick = Options.Grid.AfterRowClick;
	        }

	        if(Options.Grid && jQuery.isFunction(Options.Grid.RowDblClick))
	        {
	            B.Grid.RowDblClick = Options.Grid.RowDblClick;
	        }

            //export
	        if(jQuery.isFunction(Options.BeforeExport))
	        {
	            B.BeforeExport = Options.BeforeExport;
	        }

            //Button Click
	        if(Options.Button && jQuery.isFunction(Options.Button.BeforeClick))
	        {
	            B.Button.BeforeClick = Options.Button.BeforeClick;
	        }
			if(Options.Button && jQuery.isFunction(Options.Button.BeforeShowFilter))
	        {
	            B.Button.BeforeShowFilter = Options.Button.BeforeShowFilter;
	        }

	        return B;
	    }
	});
})(jQuery);